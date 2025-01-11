import hashlib
import shutil
from pathlib import Path
from flask import current_app as app
from werkzeug.datastructures.file_storage import FileStorage
from io import BytesIO

from CodeGuard.models import Images, ContentImages, CourseImages, db
from CodeGuard.utils.files.uploaders import FilesystemUploads, S3Uploads
import boto3
from botocore.client import Config


def get_uploader():
    upload_provider = app.config.get("UPLOAD_PROVIDER")
    if upload_provider in ("minio", "s3"): 
        return S3Uploads()
    else:
        return FilesystemUploads()
    
def get_model(type):
    model = {
        "content": ContentImages,
        "course": CourseImages,
    }
    return model.get(type, Images)
    
def get_file(filename):
    image = db.session.scalars(db.select(Images).where(Images.new_filename == filename)).first()
    if image:
        uploader = get_uploader()
        response = uploader.get_image(image.location)
        streamObj = response.get("Body").read()
        return BytesIO(streamObj)
    

        
def upload_file(file: FileStorage, usage, id=None, location=None):
    file_obj = file
    usage_for = usage
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
    location, new_filename = uploader.upload(file_obj=file_obj, filename=filename, path=parent)

    model_attrs = {
        "original_filename": filename,
        "new_filename": new_filename,
        "location": location,
    }

    model = Images
    if usage_for == "content":
        model = ContentImages
        model_attrs['content_id'] = id
    if usage_for == "course":
        model = CourseImages
        model_attrs['course_id'] = id

    existing_file = db.session.scalars(
        db.select(Images)
        .where(Images.location == location)
    ).first()
    if existing_file:
        for k, v in model_attrs.items():
            setattr(existing_file, k, v)
        db.session.commit()
        file_row = existing_file
    else: # new file
        file_row = model(**model_attrs)
        db.session.add(file_row)
        db.session.commit()

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
