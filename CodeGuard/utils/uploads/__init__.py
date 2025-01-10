import hashlib
import shutil
from pathlib import Path
from flask import current_app as app
from werkzeug.datastructures.file_storage import FileStorage

from CodeGuard.models import Images, db
from CodeGuard.utils.uploads.uploaders import FilesystemUploads, S3Uploads
import boto3
from botocore.client import Config


def get_uploader():
    upload_provider = app.config.get("UPLOAD_PROVIDER")
    if upload_provider in ("minio", "s3"): 
        return S3Uploads()
    else:
        return FilesystemUploads()
    
def stream(filename):
    uploader = get_uploader()
    response = uploader.get_image(filename)
    file_stream = response['Body']
    content_type = response.get('ContentType', 'application/octet-stream')
    
    for chunk in file_stream.iter_chunks(chunk_size=8192):
        yield chunk

def upload_file(file: FileStorage, id=None, location=None):
    file_obj = file
    content_id = id
    # challenge_id = kwargs.get("challenge_id") or kwargs.get("challenge")
    # page_id = kwargs.get("page_id") or kwargs.get("page")
    # file_type = kwargs.get("type", "standard")
    # location = kwargs.get("location")

    # Validate location and default filename to uploaded file's name
    parent = None
    filename = file_obj.filename
    if location:
        path = Path(location)
        if len(path.parts) != 2:
            raise ValueError(
                "Location must contain two parts, a directory and a filename"
            )
        # Allow location to override the directory and filename
        parent = path.parts[0]
        filename = path.parts[1]
        location = parent + "/" + filename

    
    uploader = get_uploader()
    location = uploader.upload(file_obj=file_obj, filename=filename, path=parent)

    model = Images
    model_args = {
        "original_filename": filename,
        "location": location,
        "content_id": content_id
    }
    existing_file = Images.query.filter_by(location=location).first()
    if existing_file:
        for k, v in model_args.items():
            setattr(existing_file, k, v)
        db.session.commit()
        file_row = existing_file
    else:
        file_row = model(**model_args)
        db.session.add(file_row)
        try:
            db.session.commit()
        except Exception as e:
            print('Image has no content_id!')
            uploader.delete(location)
            db.session.rollback()
    

    return file_row

def delete_file(file_id):
    f = Images.query.filter_by(id=file_id).first_or_404()

    uploader = get_uploader()
    uploader.delete(filename=f.location)

    db.session.delete(f)
    db.session.commit()
    return True


def rmdir(directory):
    shutil.rmtree(directory, ignore_errors=True)
