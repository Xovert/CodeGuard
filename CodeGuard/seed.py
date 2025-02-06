import time
import click
import os
from flask import session, current_app as app
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from werkzeug.datastructures.file_storage import FileStorage
from sqlalchemy.exc import IntegrityError as sqlerror
from freezegun import freeze_time
from sqlalchemy.orm import joinedload, lazyload, selectinload
from flask_migrate import upgrade, migrate, downgrade, stamp
from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import func

from CodeGuard.auth import bcrypt
from CodeGuard.models import (
    Users,
    CourseStatus,
    Courses,
    Enrollments,
    Modules,
    Images,
    Contents,
    ContentsLearning,
    ContentsChallenges,
    Exams,
    ExamQuestions,
    ChallengeQuestions,
    Options,
    ExamOptions,
    ChallengeOptions,
    ContentImages,
    CourseImages,
    EnrollmentsModules,
    UsersContents,
    db
)
from CodeGuard.models.enums import CompletionStatus, CourseStatus
from sqlalchemy.exc import IntegrityError as sqlerror


def hash_pass(passes):
    return bcrypt.generate_password_hash(passes)

def seed_users():
    users = [
        Users(
            uuid=uuid4(),
            role='admin',
            fullname='Admin User',
            username='admin',
            password=hash_pass('4dm!n'),  # Ensure you hash passwords appropriately
            email='admin@gmail.com',
            is_confirmed=False,
            confirmed_on=None,
            registration_date=datetime.now(timezone(timedelta(hours=7)))
        ),
        Users(
            uuid=uuid4(),
            role='user',
            fullname='John Doe',
            username='john',
            password=hash_pass('j0hn#'),
            email='john@gmail.com',
            is_confirmed=False,
            confirmed_on=None,
            registration_date=datetime.now(timezone(timedelta(hours=7)))
        ),
        Users(
            uuid=uuid4(),
            role='user',
            fullname='Jane Doe',
            username='jane',
            password=hash_pass('j@ne#'),
            email='jane@gmail.com',
            is_confirmed=False,
            confirmed_on=None,
            registration_date=datetime.now(timezone(timedelta(hours=7)))
        ),
        Users(
            uuid=uuid4(),
            role='user',
            fullname='Amandoos',
            username='scaramochi',
            password=hash_pass('sc@ram0ch!'),
            email='nathania@gmail.com',
            is_confirmed=False,
            confirmed_on=None,
            registration_date=datetime.now(timezone(timedelta(hours=7)))
        ),
        Users(
            uuid=uuid4(),
            role='user',
            fullname='Greyson',
            username='grey',
            password=hash_pass('tokora'),
            email='kora@gmail.com',
            is_confirmed=False,
            confirmed_on=None,
            registration_date=datetime.now(timezone(timedelta(hours=7)))
        ),
        Users(
            uuid=uuid4(),
            role='user',
            fullname='Black Bird',
            username='blackbird',
            password=hash_pass('21blackbird'),
            email='21blackbird@gmail.com',
            is_confirmed=False,
            confirmed_on=None,
            registration_date=datetime.now(timezone(timedelta(hours=7)))
        ),
        # Add more users as needed
    ]

    for user in users:
        db.session.add(user)
        try:
            db.session.flush()
            print(f'User {user.username} has succesfully been seeded')
        except sqlerror:
            print(f"User {user.username} already seeded")
            db.session.rollback()
        else:
            db.session.commit()
    print("Seeded Users.")

def seed_courses():
    courses = [ 
        {
            "course": Courses(
                course_name='PHP',
                duration=timedelta(days=30).total_seconds(),  # in seconds
                description='PHP is a powerful and widely-used server-side scripting language, but its popularity makes it a common target for security threats. This course, based on the OWASP Top 10 2021, focuses on secure coding practices in PHP, teaching you how to prevent vulnerabilities like SQL injection, XSS, and CSRF, and many others.',
                status=CourseStatus.PUBLISHED # Assuming 1 means active,
            ),
            "image": "php.png"
        },
        {
            "course": Courses(
                course_name='JS',
                duration=timedelta(days=30).total_seconds(),
                description='JavaScript powers modern web applications on both the client and server sides, but its ubiquity increases the risk of exploitation. This course, based on the OWASP Top 10 2021, focuses on secure coding in JavaScript, covering how to mitigate threats like XSS, CSRF, and injection attacks.',
                status=CourseStatus.PUBLISHED
            ),
            "image": "js.png"
        },
        {
            "course": Courses(
                course_name='Python',
                duration=timedelta(days=30).total_seconds(),
                description='Python is a versatile, high-level programming language popular for its readability and widespread use. However, that popularity also makes it a frequent target for security attacks. This course, aligned with the OWASP Top 10 2021, teaches secure coding practices in Python, helping you prevent vulnerabilities like injection, XSS, CSRF, and more.',
                status=CourseStatus.PUBLISHED
            ),
            "image": "python.png"
        },
        {
            "course": Courses(
                course_name='C/C++',
                duration=timedelta(days=30).total_seconds(),
                description='C and C++ offer powerful low-level control and high performance, but these features can lead to critical security flaws if not handled carefully. Guided by the OWASP Top 10 2021, this course explores safe coding techniques in C/C++, helping you prevent buffer overflows, memory corruption, injection flaws, and more.',
                status=CourseStatus.PUBLISHED
            ),
            "image": "cpp.png"
        }
        # Add more courses as needed
    ]

    for course in courses:
        db.session.add(course["course"])
        try:
            db.session.flush()
            print(f'Course {course["course"].course_name} has succesfully been seeded')
            try:
                upload_image(
                    ref_id=course["course"].id,
                    filename=course["image"], 
                    usage="course"
                )
            except FileNotFoundError as e:
                print(f"An error occcured while uploading course image:\n\t {e}")
        except sqlerror:
            print(f'Course {course["course"].course_name} already seeded')
            db.session.rollback()
        else:
            db.session.commit()

    print("Seeded Courses.")


def seed_modules():
    existing_course = db.session.scalars(
        db.select(Courses)
        .where(Courses.course_name == "PHP")
    ).first()

    modules = []
    module_names = [
        "Broken Access Control",
        "Cryptographic Failures",
        "Injection",
        "Insecure Design",
        "Security Misconfiguration",
        "Vulnerable and Outdated Components",
        "Identification and Authentication Failures",
        "Software and Data Integrity Failures",
        "Security Logging and Monitoring Failures",
        "Server-Side Request Forgery"
    ]

    for i, module_name in enumerate(module_names):
        module = Modules(
            course_id=existing_course.id,
            order=i+1,
            module_name=module_name
        )
        db.session.add(module)
        try:
            db.session.flush()
            print(f'Module {module.module_name} has succesfully been seeded')
        except sqlerror:
            print(f"Module {module.module_name} already seeded")
            db.session.rollback()
        else:
            db.session.commit()

    print("Seeded Modules.")


def seed_contents():
    modules = db.session.scalars(db.select(Modules)).all()
    module_map = {module.module_name: module for module in modules}
    
    
    #1 Broken Access Control
    module = module_map["Broken Access Control"]
    module_map["Broken Access Control"] = [
        #IDOR
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 1,
                "content_body": "Broken Access Control (BAC) adalah kategori kerentanan yang mengakibatkan penyerang dapat mengakses, memodifikasi, atau menjalankan suatu fungsi yang ada di luar batasan yang seharusnya diberikan kepada pengguna.",
                "image": 'BrokenAccessControl.png'
            },
        },
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 2,
                "content_body": "Insecure Direct Object Reference (IDOR), adalah salah satu contoh kerentanan dengan kategori BAC yang terjadi ketika penyerang dapat mengakses atau mengubah data dengan memanipulasi pengidentifikasi yang digunakan dalam URL atau parameter aplikasi web. Kerentanan ini dapat terjadi karena tidak adanya pemeriksaan kontrol akses / access control list (ACL) yang baik, sehingga gagal memverifikasi apakah pengguna diizinkan untuk mengakses data tertentu.",
                "image": None
            },
        },
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 3,
                "content_body": "Untuk mencegah IDOR, kita dapat melakukan berbagai cara seperti, selalu verifikasi bahwa pengguna memiliki izin untuk mengakses objek yang diminta",
                "image": 'IDORPrevent1.jpg'
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 4,
                "content_body": "Selain itu, hindari juga penggunaan identifier yang mudah ditebak dengan menggunakan sesuatu seperti Universally Unique Identifier (UUID)",
                "image": 'UUID.png'
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 5,
                "image": 'IDOR.png'
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Isi bagian yang kosong untuk membuat identifier yang unik berdasarkan waktu dibuatnya id untuk pengguna!",
                    "code": None,
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "uniqid()", "is_correct": True},
                    ]
                },
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 6,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Apa cara utama untuk memitigasi Insecure Direct Object Reference (IDOR)?",
                    "code": None,
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "Mengamankan objek dengan parameter tertentu", "is_correct": False},
                        {"option_text": "Menyimpan semua data pengguna di sisi klien untuk mengurangi risiko IDOR", "is_correct": False},
                        {"option_text": "Menerapkan access control checks untuk setiap objek yang coba diakses pengguna.", "is_correct": True},
                        {"option_text": "Menggunakan CAPTCHA untuk setiap permintaan data sensitif", "is_correct": False},
                    ]
                }
            },
        },

        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 7,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Apa itu Insecure Direct Object References (IDOR)?",
                    "code": None
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "Merupakan kerentanan dimana penyerang dapat mengakses atau memodifikasi data dengan cara memanipulasi id pada URL/parameter.","is_correct": True},
                        {"option_text": "Objek direk yang tidak aman", "is_correct": False},
                        {"option_text": "Objek tertentu di aplikasi web yang tidak dienkripsi dengan benar","is_correct": False},
                        {"option_text": "Jenis serangan di mana hacker menggunakan SQL Query untuk mendapatkan akses langsung ke database aplikasi","is_correct": False}
                    ]
                }
            },
        },
        
        #Path Traversal
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 8,
                "content_body": "Path Traversal, atau biasa disebut juga directory traversal adalah kerentanan yang memungkinkan penyerang untuk mengakses file dan direktori yang disimpan di luar folder utama dari website file.",
                "image": None
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 9,
                "content_body": "Kita dapat mencegah path traversal dengan cara validasi dan sanitasi user input menggunakan fungsi realpath()",
                "image": 'PathTraversal.png'
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 10,
                "image": 'PathTraversalITB.png'
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Isi bagian yang kosong untuk mencegah terjadinya serangan path traversal! Gunakan function yang ada pada PHP!",
                    "code": None
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "realpath($filePath);", "is_correct": True},
                    ]
                }
            },

        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 11,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Skenario: Aplikasi Anda memiliki URL seperti http://example.com/view?file=report.txt. Namun, seorang penyerang mencoba mengakses file /etc/passwd menggunakan URL berikut:\nhttp://example.com/view?file=../../../../etc/passwd. Apa langkah terbaik untuk mencegah serangan ini?",
                    "code": None
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "Gunakan HTTPS untuk mengenkripsi komunikasi", "is_correct": False},
                        {"option_text": "Validasi dan sanitasi input pengguna untuk mencegah akses file di luar direktori yang diizinkan", "is_correct": True},
                        {"option_text": "Berikan hak akses root ke aplikasi agar dapat membaca file penting", "is_correct": False},
                        {"option_text": "Sembunyikan URL aplikasi dari pengguna", "is_correct": False}
                    ]
                }
            },
        }

    ]

    #2 Cryptographic Failures
    module = module_map["Cryptographic Failures"]
    module_map["Cryptographic Failures"] = [
        #Hard-Coded Cryptographic Key
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 1,
                "content_body": "Cryptographic Failures merupakan kategori kerentanan yang terkait erat dengan kegagalan penggunaan / implementasi kriptografi pada data yang harusnya dilindungi. Kerentanan ini biasanya menyebabkan terungkapnya data sensitif. Contoh dari kerentanan ini adalah Hard-Coded Cryptographic Key dan Use of one-way hash without a salt or with predictable salt",
                "image": 'cryptographicfailure.png'
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 2,
                "content_body": "Hard-Coded Cryptographic Key, adalah praktik penyimpanan cryptography key di dalam source code. Hal ini berbahaya karena attacker dapat menemukan dan mengeksplotasi key tersebut. Data sensitif yang dilindungi dengan key tersebut dapat dengan mudah didekripsi.",
                "image": 'HardCodedKey.png'
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 3,
                "content_body": "Untuk menghindari hal tersebut kita dapat mengimplementasikan penyimpanan cryptography key pada file .env atau penggunaan Key Management Service (KMS). Pada PHP sendiri, terdapat library phpdotenv yang dapat membantu dalam penyimpanan cryptography key dalam file .env",
                "image": 'phpdotenv.png'
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 4,
                "image": 'phpdotchal.png'
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Isi bagian kosong pada potongan kode berikut untuk menggunakan dotenv!",
                    "code": None,
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "load();", "is_correct": True},
                    ]
                }
            },
        },
        
        #Use of one-way hash without a salt or with predictable salt
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 5,
                "content_body": "Penggunaan algoritma hash yang baik kurang cukup untuk melindungi password. Penyerang tetap bisa mendapatkan password dengan melakukan teknik serangan rainbow tables. Untuk itu, kita perlu menambahkan salt dan pepper pada teknik hashing yang kita gunakan.",
                "image": 'saltpaper.png'
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 6,
                "image": 'saltpaperchal.png'
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Isi bagian kosong pada potongan kode berikut untuk membuat hash dengan salt dan pepper!",
                    "code": None,
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "generateSalt();", "is_correct": True},
                    ]
                }
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 7,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Apa perbedaan utama antara salt dan pepper dalam konteks keamanan hashing password?",
                    "code": None
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "Salt bersifat unik untuk setiap password, sedangkan pepper adalah nilai rahasia yang sama untuk semua password.", "is_correct": True},
                        {"option_text": "Salt adalah algoritma hashing yang lebih kuat, sedangkan pepper adalah algoritma tambahan untuk enkripsi.", "is_correct": False},
                        {"option_text": "Salt digunakan untuk mengenkripsi password, sedangkan pepper digunakan untuk mendekripsi password.", "is_correct": False},
                        {"option_text": "Salt meningkatkan panjang hash secara acak, sedangkan pepper mengurangi panjang hash agar lebih cepat diproses.", "is_correct": False}
                    ]
                }
            },
        },

        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 8,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Apa risiko utama ketika menggunakan one-way hash tanpa salt dalam menyimpan password pengguna?",
                    "code": None
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "Penggunaan memori menjadi lebih efisien karena tidak ada tambahan data.", "is_correct": False},
                        {"option_text": "Password yang sama akan menghasilkan hash yang sama, sehingga rentan terhadap serangan tabel pelangi (rainbow table).", "is_correct": True},
                        {"option_text": "Kecepatan hashing meningkat karena tidak perlu menghitung tambahan salt.", "is_correct": False},
                        {"option_text": "Memastikan keamanan tambahan dengan mengurangi kompleksitas.", "is_correct": False}
                    ]
                }
            },
        }

    ]
    
    #3 Injection
    module = module_map["Injection"]
    module_map["Injection"] = [
        
        #SQL Injection
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 1,
                "content_body": "Injection merupakan kategori kerentanan dimana penyerang memasukkan payload, file, ataupun query ke dalam suatu input dalam website. Serangan paling umum dari kategori ini adalah: SQL Injection dan Cross Site Scripting (XSS)",
                "image": None
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 2,
                "content_body": "SQL Injection adalah kerentanan dimana penyerang mengeksploitasi input dalam aplikasi untuk menjalankan perintah SQL",
                "image": None
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 3,
                "content_body": "Pencegahan utama SQL injection adalah prepare statements. Prepare statements adalah teknik dalam SQL yang memungkinkan pengembang memisahkan logika kueri dari data input pengguna. Dengan cara ini, kueri SQL menjadi lebih aman, efisien, dan dapat digunakan kembali, sekaligus mencegah risiko injeksi SQL",
                "image": 'PrepareStatement.png'
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 4,
                "content_body": "Selain itu, kita juga dapat implementasikan validasi dan sanitasi input. Pastikan input yang dimasukkan sesuai dengan keinginan kita. Misalnya jika login menggunakan email, maka validasi input sebagai email dan sanitasi agar tidak ada karakter berbahaya yang dapat ikut masuk.",
                "image": 'ValidSanitSQL.png'
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 5,
                "image": 'SQLIfitb.png'
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Isi bagian yang kosong dengan kode untuk membuat prepare statement!",
                    "code": None,
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "$stmt->bindParam('s', $item);", "is_correct": True},
                    ]
                }
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 6,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Pilihlah baris kode mana yang paling cocok untuk melengkapi prepare statement berikut untuk menghindari serangan SQLInjection!",
                    "code": None
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "$stmt->execute();", "is_correct": True},
                        {"option_text": "$stmt->run();", "is_correct": False},
                        {"option_text": "$stmt->operate();", "is_correct": False},
                        {"option_text": "$stmt->execute(':username'; ':password');", "is_correct": False}
                        ]
                    }
            },
        },
    
    #XSS
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 7,
                "content_body": "XSS Injection, atau Cross-Site Scripting adalah serangan dimana skrip berbahaya dimasukan ke input dalam web. Hal ini dapat terjadi karena kurang baiknya validasi input pada web.",
                "image": None
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 8,
                "content_body": "Untuk mencegah terjadinya XSS, kita dapat melakukan beberapa hal seperti mengimpementasikan encoding. Pada php sendiri, terdapat suatu function yang dapat melakukan hal tersebut, yaitu htmlspecialchars().",
                "image": 'htmlspecialchars.png'
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 9,
                "image": 'XSSfitb.png'
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Isi bagian yang kosong dengan kode agar output dari $safestring menjadi “&lt;script&gt;alert('XSS);&lt;/script&gt;” !",
                    "code": None,
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "htmlspecialchars", "is_correct": True},
                    ]
                }
            },
        },
    
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 10,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Untuk menghindari serangan XSS, apa yang harus dilakukan?",
                    "code": None
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "input encoding", "is_correct": True},
                        {"option_text": "gunakan http header X-Frame-Options", "is_correct": False},
                        {"option_text": "implementasikan rate-limit", "is_correct": False},
                        {"option_text": "implementasikan captcha", "is_correct": False}
                    ]
                }
            },
        },

        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 11,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Dalam XSS, apa yang diinject ke dalam input field?",
                    "code": None
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "command", "is_correct": False},
                        {"option_text": "query", "is_correct": False},
                        {"option_text": "script", "is_correct": True},
                        {"option_text": "semuanya benar", "is_correct": False}
                    ]
                }
            },
        }

    ]
    
    #4 Insecure Design
    module = module_map["Insecure Design"]
    module_map["Insecure Design"] = [
        #no rate limit
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 1,
                "content_body": "Insecure Design adalah sebuah kategori resiko keamanan yang mencakup tidak efektifnya atau bahkan tidak adanya sistem keamanan dalam desain aplikasi. Dengan kata lain, Insecure Design adalah masalah konseptual",
                "image": None
            },
        },
       
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 2,
                "content_body": "Desain yang tidak aman mencakup beberapa hal misalnya No rate-limit dan exposure of sensitive information.",
                "image": None
            },
        },
       
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 3,
                "content_body": "No rate-limit merupakan kerentanan yang berkaitan juga dengan kategori identification and authentication failures. Dengan menggunakan rate-limit, kita membatasi berapa kali user dapat mencoba untuk login. Jika user login lebih dari batasan yang kita berikan, kita lock fitur login mereka. Hal ini dibutuhkan sebagai langkah preventif serangan brute-force.",
                "image": 'RateLimit.png'
            },
        },
       
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 4,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Mengapa no-rate limit pada halaman login dapat berisiko bagi sistem keamanan?",
                    "code": None
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "Membuat pengguna dapat mengakses akun mereka tanpa masalah", "is_correct": False},
                        {"option_text": "Memberikan kesempatan bagi penyerang untuk mencoba password yang berbeda dalam jumlah banyak", "is_correct": True},
                        {"option_text": "Menyebabkan halaman login menjadi lebih cepat dan efisien", "is_correct": False},
                        {"option_text": "Mengurangi kebutuhan akan verifikasi dua faktor", "is_correct": False}
                    ]
                }
            },
        },

        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 5,
                "image": 'RateLimitChal.png'
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Isi bagian yang kosong dengan kode untuk membuat rate limit dengan maksimum percobaan login 5 dan lockout time 300 detik!",
                    "code": None,
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "$lockout_time", "is_correct": True},
                    ]
                }
            },
        },
    
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 6,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Apa sebenarnya yang dimaksud dengan \"rate limit\" dalam konteks aplikasi web?",
                    "code": None
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "Pembatasan jumlah data yang dapat diunggah oleh pengguna", "is_correct": False},
                        {"option_text": "Pembatasan jumlah permintaan (request) yang dapat dilakukan oleh pengguna dalam periode waktu tertentu", "is_correct": True},
                        {"option_text": "Pembatasan jumlah pengguna yang dapat login dalam satu waktu", "is_correct": False},
                        {"option_text": "Pembatasan panjang password yang dapat digunakan oleh pengguna", "is_correct": False}
                    ]
                }
            },
        },
    
    #Exposure of sensitive information
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 7,
                "content_body": "Exposure of sensitive information merupakan kerentanan dimana informasi sensitif terpampang dikarenakan fungsionalitas dalam aplikasi. Pada saat mengembangkan aplikasi, desain aplikasi juga harus mempertimbangkan informasi apa yang sensitif dan harus dilindungi.",
                "image": 'Exposure.png'
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 8,
                "content_body": "Untuk mencegah terjadinya exposure of sensitive information, kita dapat mencegahnya dengan mengimplementasikan enkripsi pada data sensitive dan juga validasi dan sanitasi input. Untuk melakukan validasi dan sanitasi dalam PHP sendiri, terdapat fungsi filter_var()",
                "image": 'encryptexpose.png'
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 9,
                "image": 'FilterEmail.png'
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Isi bagian yang kosong dengan kode yang tepat untuk membuat validasi dan sanitasi untuk input email!",
                    "code": None,
                },
                "options": {
                        "model": ChallengeOptions,
                        "rows": [
                            {"option_text": "FILTER_SANITIZE_EMAIL", "is_correct": True},
                        ]
                }
            },
        },
    
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 10,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Manakah dari berikut ini yang dapat meningkatkan risiko Exposure of Sensitive Information ?",
                    "code": None
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "Menggunakan HTTPS untuk komunikasi data", "is_correct": False},
                        {"option_text": "Menyimpan password pengguna dalam bentuk teks biasa (plain text) di database", "is_correct": True},
                        {"option_text": "Memastikan setiap sesi pengguna terlindungi dengan session ID yang kuat", "is_correct": False},
                        {"option_text": "Mengimplementasikan validasi input untuk mencegah SQL injection", "is_correct": False}
                    ]
                }
            },
        } 
    ]
    
    #5 Security Misconfiguration
    module = module_map["Security Misconfiguration"]
    module_map["Security Misconfiguration"] = [
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 1,
                "content_body": "Security Misconfiguration adalah kategori kerentanan yang diakibatkan oleh kesalahan atau tidak adanya konfigurasi keamanan dalam web, application frameworks, databases, atau software. Selain itu, penggunaan konfigurasi yang tidak dibutuhkan dan membuat keamanan terancam juga masuk  ke dalam kategori ini.",
                "image": None
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 2,
                "content_body": "contoh kerentanan dari Security Misconfiguration adalah XML External Entities (XXE) dan HTTP Header Misconfigurations.",
                "image": None
            },
        },
        
        #XML External Entities (XXE)
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 3,
                "content_body": "XML External Entities (XXE), adalah jenis serangan yang menargetkan aplikasi yang memproses input XML. Serangan ini memanfaatkan kelemahan dalam konfigurasi parser XML.",
                "image": None
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 4,
                "content_body": "Utamanya, untuk mencegah XXE, kita bisa mematikan penggunaan DTD (external entities) jika tidak diperlukan serta implementasi sanitasi input agar tidak dapat menerima / memproses XML command. Pada PHP, kita dapat menggunakan library berikut untuk mematikan penggunaan external entities.",
                "image": None
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 5,
                "content_body": "Untuk PHP versi 8 ke bawah, gunakan libxml_disable_entity_loader()",
                "image": 'phpdiatas.png'
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 6,
                "content_body": "Untuk PHP versi di atas 8, gunakan libxml_set_external_entity_loader()",
                "image": 'phpdibawah.png'
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 7,
                "image": 'libxml.png'
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Isi bagian kosong pada potongan kode berikut untuk mematikan DTD loading secara total pada PHP dengan versi di atas 8!",
                    "code": None,
                },
                "options": {
                        "model": ChallengeOptions,
                        "rows": [
                            {"option_text": "set_external_entity_loader(null);", "is_correct": True},
                        ]
                }
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 8,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Bagaimana cara menghindari serangan XML External Entities (XXE) dalam PHP?",
                    "code": None
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "Menggunakan fungsi simplexml_load_file() untuk membaca XML dari sumber tidak tepercaya", "is_correct": False},
                        {"option_text": "Menonaktifkan pengolahan entitas eksternal saat mem-parsing XML menggunakan set_external_entity_loader(null)", "is_correct": True},
                        {"option_text": "Menggunakan format lain seperti JSON untuk menggantikan XML", "is_correct": False},
                        {"option_text": "Menyimpan file XML di server tanpa validasi apa pun", "is_correct": False}
                    ]
                }
            },
        },
    
        #HTTP Header Misconfigurations
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 9,
                "content_body": "HTTP Header Misconfiguration, penggunaan HTTP header yang tepat dapat menjadikan keamanan web lebih terjaga. Kesalahan atau tidak adanya konfigurasi HTTP header dapat mengakibatkan banyak jenis kerentanan.",
                "image": None
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 10,
                "content_body": "Beberapa jenis HTTP Header yang dapat kita konfigurasi antara lain adalah X-Frame-Options (untuk mencegah clickjacking); X-Content-Type-Options (mencegah MIME type confusion); X-Powered-By (untuk mencegah terungkapnya informasi mengenai framework, bahasa pemrograman, atau server yang digunakan.)",
                "image": None
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 11,
                "content_body": "Pada PHP, untuk melakukan konfigurasi HTTP header, kita dapat menggunakan function header(). Sedangkan untuk menghapus HTTP header kita dapat menggunakan header_remove()",
                "image": None
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 12,
                "image": 'anticlickjack.png'
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Isi bagian kosong pada potongan kode berikut untuk memastikan serangan click-jacking tidak dapat dilakukan!",
                    "code": None,
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "X-Frame-Options: DENY", "is_correct": True},
                    ]
                }
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 13,
                "image": 'antiexpose.png'
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Isi bagian yang kosong pada potongan kode berikut untuk memastikan teknologi sisi server pada aplikasi web tidak dapat diketahui melalui HTTP header!",
                    "code": None,
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "X-Powered-By", "is_correct": True},
                    ]
                }
            },
        },
    ]
    
    #6 Vulnerable and Outdated Components
    module = module_map["Vulnerable and Outdated Components"]
    module_map["Vulnerable and Outdated Components"] = [
         {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 1,
                "content_body": "Vulnerable and Outdated Components, adalah kategori kerentanan yang terjadi ketika komponen software yang digunakan dalam aplikasi tidak diperbarui atau memiliki kerentanan, sehingga membuka celah bagi penyerang untuk mengeksploitasi sistem. Komponen – komponen yang dimaksud antara lain adalah software, libraries, frameworks, dan dependencies.",
                "image": None
            },
        },
         
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 2,
                "content_body": "Untuk mencegah adanya vulnerable dan outdate components, developer harus selalu mengecek software, libraries, frameworks dan dependencies yang akan dipakai apakah berbahaya / outdated atau tidak.",
                "image": None
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 3,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Apa yang dimaksud dengan Vulnerable and Outdated Components dalam konteks aplikasi web?",
                    "code": None
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "Komponen yang tidak dapat diperbarui karena ketergantungan sistem", "is_correct": False},
                        {"option_text": "Komponen perangkat keras yang tidak kompatibel dengan aplikasi web", "is_correct": False},
                        {"option_text": "Komponen perangkat lunak dalam aplikasi yang memiliki celah keamanan atau tidak diperbarui ke versi terbaru", "is_correct": True},
                        {"option_text": "Komponen yang tidak memerlukan pembaruan untuk tetap berfungsi dengan baik", "is_correct": False}
                    ]
                }
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 4,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Apa yang seharusnya dilakukan pengembang setelah mengidentifikasi komponen yang rentan atau usang dalam aplikasi PHP?",
                    "code": None
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "Menghentikan aplikasi dan melaporkan masalah ke pihak ketiga", "is_correct": False},
                        {"option_text": "Segera mengupdate atau mengganti komponen yang rentan dengan versi yang lebih baru dan aman", "is_correct": True},
                        {"option_text": "Menunggu sampai masalah menjadi lebih besar sebelum mengupdate", "is_correct": False},
                        {"option_text": "Membiarkan komponen usang tetap digunakan karena tidak menyebabkan masalah langsung", "is_correct": False}
                    ]
                }
            },
        }
        
    ]

    #7 Identification and Authentication Failures
    module = module_map["Identification and Authentication Failures"]
    module_map["Identification and Authentication Failures"] = [
        #
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 1,
                "content_body": "Identification and Authentication Failures, adalah kategori kerentanan yang diakibatkan kurang baiknya penerapan proses identifikasi dan autentikasi dalam suatu sistem. Kegagalan dalam proses tersebut memungkinkan penyerang mendapatkan akses tidak sah ke dalam sistem atau data sensitif.",
                "image": None
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 2,
                "content_body": "Beberapa contoh kerentanan dalam kategori ini ada Permits of default or weak passwords dan juga Exposes session identifier in the URL.",
                "image": None
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 3,
                "content_body": "Permits of default or weak passwords, kata kunci atau password yang baik  adalah kata kunci yang susah ditebak baik secara manual maupun ditebak menggunakan automated tools. Kata kunci yang kuat harus kompleks, panjang, dan tidak dapat diprediksi. Dengan mengizinkan penggunaan kata kunci yang lemah, dapat mengakibatkan akses tidak sah. Kata kunci yang lemah misalnya adalah Password1 atau admin/admin.",
                "image": None
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 4,
                "content_body": "Untuk mencegah hal tersebut, kita dapat mengimplementasikan pengecekan terhadap input password pengguna",
                "image": 'strongpass.png'
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 5,
                "image": 'strlen.png'
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Isi bagian kosong pada potongan kode berikut untuk membuat pengecekan panjang karakter dari input $password user! Buat input password user harus lebih dari 8 karakter!",
                    "code": None,
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "strlen($password) < 8", "is_correct": True},
                    ]
                }
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 6,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Apa yang dimaksud dengan weak password?",
                    "code": None
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "Password yang panjang dan kompleks", "is_correct": False},
                        {"option_text": "Password yang mudah ditebak dan menggunakan kombinasi yang sederhana (misalnya, 123456 dan password)", "is_correct": True},
                        {"option_text": "Password yang tidak dapat ditebak", "is_correct": False},
                        {"option_text": "Password yang susah untuk diingat", "is_correct": False}
                    ]
                }
            },
        },
        
        #Exposes session identifier in the URL
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 7,
                "content_body": "Exposes session identifier in the URL, merupakan kerentanan dimana session ID terpampang dalam URL. Hal ini memungkinkan penyerang untuk mendapatkan hak akses dari akun yang session ID-nya dicuri.",
                "image": 'sessionSteal.png'
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 8,
                "content_body": "Terdapat beberapa cara pencegahan dari exposes session identifier in the URL, salah satunya adalah dengan mengimplmentasikan cookie untuk menyimpan session ID",
                "image": 'cookie.png'
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 9,
                "content_body": "Setup cookie pada file php.ini (global configuration file for php)",
                "image": 'cookieCode.png'
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 10,
                "image": 'cookieChal.png'
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Isi bagian kosong pada potongan kode berikut untuk mengatur cookie agar valid sampai 5 jam setelah user login!",
                    "code": None,
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "1800", "is_correct": True},
                    ]
                }
            },
        },
      
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 11,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Mengapa \"Exposes session identifier in the URL\" dianggap sebagai risiko keamanan?",
                    "code": None
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "Karena session ID yang terdapat dalam URL dapat dilihat dan dicuri oleh pihak yang tidak berwenang", "is_correct": True},
                        {"option_text": "Karena session ID terenkripsi di dalam URL, sehingga tidak dapat diakses oleh pengguna lain.", "is_correct": False},
                        {"option_text": "Exposes session identifier in the URL bukan merupakan risiko keamanan", "is_correct": False},
                        {"option_text": "Karena session ID yang disembunyikan dalam URL lebih aman daripada menggunakan cookie.", "is_correct": False}
                    ]
                }
            },
        },

    ]

    #8 Software and Data Integrity Failures
    module = module_map["Software and Data Integrity Failures"]
    module_map["Software and Data Integrity Failures"] = [
         {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 1,
                "content_body": "Software and Data Integrity Failures, adalah kategori kerentanan yang muncul karena adanya kegagalan dalam sisi software integrity maupun data integrity.",
                "image": None
            },
        },
         
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 2,
                "content_body": "Software integrity memastikan kode software tidak dimodifikasi atau dimanipulasi secara tidak sah. Sedangkan data integrity memastikan bahwa data yang disimpan atau dikirim tidak diubah atau dirusak secara tidak sah.",
                "image": None
            },
        },
         
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 3,
                "content_body": "Contoh kerentanan dalam kategori adalah Insecure Deserialization. Insecure Deserialization, merupakan kerentanan keamanan yang terjadi ketika saat data yang telah diserialisasi (misalnya, objek atau struktur data yang dikonversi ke format tertentu untuk disimpan atau dikirim) tidak diperlakukan dengan aman saat dide-serialisasi kembali ke dalam objek atau struktur aslinya. Kerentanan ini memungkinkan penyerang untuk mengeksekusi kode berbahaya, mendapatkan akses tidak sah, atau mengubah perilaku aplikasi.",
                "image": None
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 4,
                "content_body": "Untuk mencegah kerentanan ini terjadi dalam PHP, kita dapat melakukan beberapa hal seperti menghindari penggunaan fungsi unserialize() dan gunakan Gunakan format serialisasi yang lebih aman seperti JSON (json_encode / json_decode) untuk menyimpan dan membaca data.",
                "image": None
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 5,
                "content_body": "Tapi jika harus menggunakan fungsi unserialize(), pastikan  pastikan data yang di-deserialize berasal dari sumber yang terpercaya.",
                "image": None
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 6,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Manakah dari tindakan berikut yang bisa membantu mencegah masalah insecure deserialization dalam aplikasi PHP?",
                    "code": None
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "Menggunakan fungsi serialize() dan unserialize() tanpa validasi input pengguna.", "is_correct": False},
                        {"option_text": "Menggunakan metode enkripsi untuk semua data yang diserialisasi dan deserialisasi.", "is_correct": False},
                        {"option_text": "Menggunakan fungsi unserialize() hanya pada data yang berasal dari sumber tepercaya dan terverifikasi.", "is_correct": True},
                        {"option_text": "Mengandalkan PHP untuk secara otomatis memvalidasi data yang diserialisasi.", "is_correct": False}
                    ]
                }
            },
        },

        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 7,
                "image": 'diencode.png'
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Lengkapi bagian kosong pada potongan kode berikut untuk deserialisasi data yang telah diencode menggunakan json_encode()!",
                    "code": None,
                },
                "options": {
                        "model": ChallengeOptions,
                        "rows": [
                            {"option_text": "json_decode()", "is_correct": True},
                        ]
                }
            },
        },
    ]

    #9 Security Logging and Monitoring Failures
    module = module_map["Security Logging and Monitoring Failures"]
    module_map["Security Logging and Monitoring Failures"] = [
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 1,
                "content_body": "Security Logging and Monitoring Failures, adalah kategori kerentanan yang terjadi akibat adanya langkah yang tidak aman dalam mekanisme logging dan monitoring pada suatu aplikasi.",
                "image": None
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 2,
                "content_body": "Salah satu contoh kerentanan yang masuk ke dalam kategori ini adalah Insertion of Sensitive Information into Log File.	Insertion of Sensitive Information into Log File, adalah kerentanan yang terjadi saat aplikasi menuliskan data sensitif, seperti kata sandi, API key, atau data kredensial langsung ke dalam log.",
                "image": None
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 3,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Manakah dari hal berikut yang dapat membantu mengurangi kebocoran informasi sensitif melalui log file?",
                    "code": None
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "Mengaktifkan log_errors = 1 dan display_errors = 1 di file konfigurasi PHP.", "is_correct": False},
                        {"option_text": "Penggunaan error_log() untuk mencatat hanya pesan kesalahan umum tanpa detail sensitif.", "is_correct": True},
                        {"option_text": "Menyimpan file log di lokasi yang mudah diakses oleh pengguna dan pengembang.", "is_correct": False},
                        {"option_text": "Menyimpan informasi sensitif, seperti kata sandi, dalam file log untuk tujuan audit.", "is_correct": False}
                    ]
                }
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 4,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Mengapa penting untuk menghindari penyisipan informasi sensitif ke dalam log file dalam aplikasi PHP?",
                    "code": None
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "Karena file log dapat diakses oleh pihak yang tidak berwenang, mengungkapkan data yang seharusnya dirahasiakan.", "is_correct": True},
                        {"option_text": "Agar file log tidak terlalu besar dan lebih mudah diproses.", "is_correct": False},
                        {"option_text": "Agar proses debug lebih cepat dilakukan tanpa memerlukan banyak data.", "is_correct": False},
                        {"option_text": "Untuk memastikan bahwa informasi dalam log dapat diakses oleh pengembang dengan mudah.", "is_correct": False}
                    ]
                }
            },
        }
    ]

    #10 Server-Side Request Forgery
    module = module_map["Server-Side Request Forgery"]
    module_map["Server-Side Request Forgery"] = [
        #This is where you left
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 1,
                "content_body": "Server-Side Request Forgery (SSRF) adalah kerentanan dimana penyerang membuat request tidak sah atas nama suatu server ke server lain. SSRF dapat terjadi ketika web-app mengambil resource dari tempat lain tanpa memvalidasi URL yang diberikan pengguna.",
                "image": None
            },
        },
        
        {
            "model": ContentsLearning,
            "attributes": {
                "module_id": module.id,
                "order": 2,
                "content_body": "Untuk mencegah SSRF, lakukan: Sanitasi dan validasi semua input dari client-side, Jangan pernah kirimkan respon mentah ke client-side, Nonaktifkan HTTP redirect, Validasi url schema, destinasi dan port ke tempat yang hanya diizinkan menggunakan whitelist.",
                "image": None
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 3,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Apa yang dimaksud dengan Server-Side Request Forgery (SSRF)?",
                    "code": None
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "Sebuah serangan yang memungkinkan penyerang mengakses data lokal pada perangkat korban.", "is_correct": False},
                        {"option_text": "Sebuah serangan di mana penyerang memanipulasi server untuk melakukan permintaan HTTP ke lokasi yang tidak diinginkan.", "is_correct": True},
                        {"option_text": "Sebuah teknik untuk mengelabui pengguna agar memberikan informasi pribadi melalui email.", "is_correct": False},
                        {"option_text": "Sebuah serangan di mana kode berbahaya disisipkan ke dalam input form HTML.", "is_correct": False}
                    ]
                }
            },
        },
        
        {
            "model": ContentsChallenges,
            "attributes": {
                "module_id": module.id,
                "order": 4,
                "image": None
            },
            "questions": {
                "model": ChallengeQuestions,
                "attributes": {
                    "question_text": "Manakah teknik mitigasi berikut yang TIDAK efektif untuk mencegah SSRF?",
                    "code": None
                },
                "options": {
                    "model": ChallengeOptions,
                    "rows": [
                        {"option_text": "Membatasi permintaan HTTP ke domain eksternal tertentu menggunakan whitelist.", "is_correct": False},
                        {"option_text": "Menggunakan validasi input untuk memastikan URL sesuai format yang diizinkan.", "is_correct": False},
                        {"option_text": "Memblokir semua permintaan HTTP yang menggunakan protokol HTTPS.", "is_correct": True},
                        {"option_text": "Menggunakan library cURL dengan konfigurasi CURLOPT_FOLLOWLOCATION diatur ke false.", "is_correct": False}
                    ]
                }
            },
        }
        
    ]

    
    for name, contents in module_map.items():
        if type(contents) is Modules:
            continue
        print(f'Seeding module {name}...')
        for content in contents:
            add_content(**content)

    print("Seeded Contents.")


def add_content(model, attributes: dict, questions=None):
    filename = None
    if attributes.get("image"):
        filename = attributes.pop("image")

    content = model(**attributes)
    try:
        db.session.add(content)
        db.session.flush()
    except sqlerror:
        print(f'Content number:{content.order} already added')
        db.session.rollback()
        db.session.commit()
        return
    else:
        db.session.commit()
    

    if filename:
        try:
            upload_image(content.id, filename, "content")
        except FileNotFoundError as e:
            print(f'An Error occured while uploading a content image:\n\t {e}')
    
    if questions:
        questions["attributes"]["content_id"] = content.id
        add_questions(**questions)
        return


def add_questions(model, attributes: dict, options=None):
    question = model(**attributes)

    try:
        db.session.add(question)
        db.session.flush()
    except sqlerror:
        print(f'Question for {question.content_id} already added')
        db.session.rollback()
    
    if options:
        for option in options["rows"]:
            option["question_id"] = question.id
        add_options(**options)
        return
    db.session.commit()

    
def add_options(model, rows):
    for row in rows:
        new_row = model(**row)
        try:
            db.session.add(new_row)
            db.session.flush()
        except sqlerror:
            print(f'Option {new_row.option_text} for {new_row.question_id} already added')
            db.session.rollback()
        else:
            db.session.commit()
    
    return



def upload_image(ref_id, filename, usage=None):
    from CodeGuard.utils.files import upload_file
    import mimetypes
    base = app.root_path
    path = os.path.join(base, 'images', filename)
    if not os.path.isfile(path):
        raise FileNotFoundError(f'No such file: {path}')
    
    mime_type, _ = mimetypes.guess_type(path)
    if mime_type is None:
        # Default to binary stream if MIME type cannot be determined
        mime_type = 'application/octet-stream'

    file_stream = open(path, 'rb')
    file_storage = FileStorage(
        stream=file_stream,
        filename=filename,
        content_type=mime_type
    )

    upload_file(
        file=file_storage, 
        id=ref_id, 
        usage=usage
    )


def seed_enrollments():
    courses = db.session.scalars(db.select(Courses)).all()
    users = db.session.scalars(
        db.select(Users)
        .where(Users.role != 'admin')
    ).all()

    if not users or not courses:
        print("No users or courses found. Cannot seed enrollments.")
        return

    import random
    for _ in range(10):
        # Pick a random user and a random course
        user = random.choice(users)
        course = random.choice(courses)

        # Create an Enrollment object
        tz = timezone(timedelta(hours=7))
        curr_time = datetime.now(tz=tz)
        enrollment = Enrollments(
            user_id=user.id,
            course_id=course.id,
            enrollment_date=curr_time,  # Localized datetime
            progress=0,
            last_accessed_time=curr_time.timetz(), # Time only, extracted from datetime
            status=CompletionStatus.STARTED
        )
        db.session.add(enrollment)
        try:
            db.session.flush()
            print(f"Enrollment for User {enrollment.user_id}; Course {enrollment.course_id} success")
        except sqlerror:
            db.session.rollback()
            print(f"Enrollment for User {enrollment.user_id}; Course {enrollment.course_id} failed")
        else:
            db.session.commit()

    return

def seed_enrollments_modules():
    enrollments_modules = db.session.execute(
        db.select(Enrollments.id, Modules.id, Modules.order)
        .join(Enrollments.course)
        .join(Courses.module)
        .order_by(Enrollments.id)
        .order_by(Modules.id)
    ).all()

    for enrollment, module, order in enrollments_modules:
        enrollment_module = EnrollmentsModules(
            enrollment_id =  enrollment,
            module_id = module,
            progress = 1 if order == 1 else 0,
            status = CompletionStatus.STARTED if order == 1 else CompletionStatus.NOT_STARTED
        )
        db.session.add(enrollment_module)
        try:
            db.session.flush()
            print(f"Enrollment_id: {enrollment} and module: {module} order: {order} seeded")
        except sqlerror:
            db.session.rollback()
            print(f"Enrollment_id: {enrollment} and module: {module} order: {order} failed to seed")
        else:
            db.session.commit()


def seed_users_contents():
    users_contents = db.session.execute(
        db.select(EnrollmentsModules.id, Contents.id)
        .join(EnrollmentsModules.module)
        .join(Contents)
    ).all()
    i = 0
    for enrollment_module, content in users_contents:
        user_content = UsersContents(
            enrollment_module_id = enrollment_module,
            content_id = content,
            status = CompletionStatus.STARTED if i == 0 else None
        )
        db.session.add(user_content)
        try:
            db.session.flush()
            print(f"Enrollment_Module_id: {enrollment_module} and challenge: {content} seeded")
        except sqlerror:
            db.session.rollback()
            print(f"Enrollment_Module_id: {enrollment_module} and challenge: {content} failed")
        else:
            db.session.commit()
        i = i+1


def seed_exams():
    pass


def seed_all():
    seed_users()
    seed_courses()
    seed_modules()
    seed_contents()
    seed_enrollments()
    seed_enrollments_modules()
    seed_users_contents()
    seed_exams()
    db.session.close()
    click.echo('Seeded the database')

def reset():
    db.drop_all()
    db.session.commit()
    stamp(revision='base')
    click.echo('Dropped tables')

    upgrade()
    click.echo('Recreated all tables')

def reseed():
    reset()
    seed_all()


@click.command('query')
@click.argument('id', type=int)
def test_query(id):
    user_uuid = db.session.scalar(db.select(Users.uuid).where(Users.id == id))
    course_name = "PHP"
    module_name = "Broken Access Control"
    content_id = 5
    enrollment_id = db.session.scalars(
        db.select(Enrollments.id)
        .join(Users)
        .join(Courses)
        .where(Users.uuid == user_uuid)
        .where(Courses.course_name == course_name)
    ).first()
    module_id = db.session.scalar(
        db.select(Modules.id)
        .where(Modules.module_name == module_name)
    )
    course_id = db.session.scalar(
        db.select(Courses.id)
        .where(Courses.course_name == course_name)
    )
    # stmt = (
    #     db.select()
    # )
    # results = db.session.scalar(query)
    # print(query)
    # print(results.first)
    # print(results.pages)
    # print(results.last)
    # print(results.total)
    # print(type(content.question.options.pop()))
    # print(content)
    from sqlalchemy.orm.collections import InstrumentedList
    from typing import List
    # for content, in results:
    #     print(content.type)
    #     if content.image:
    #         print(content.image)

@click.command('seed')
def seed_command():
    seed_all()

@click.command('reset')
def reset_command():
    reset()

@click.command('reseed')
def reseed_command():
    reseed()

def init_seed(app):
    app.cli.add_command(seed_command)
    app.cli.add_command(reset_command)
    app.cli.add_command(reseed_command)
    app.cli.add_command(test_query)
    
#flask seed 
