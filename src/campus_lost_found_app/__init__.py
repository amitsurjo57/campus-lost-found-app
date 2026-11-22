import mysql.connector
import json
from fastapi import FastAPI, HTTPException, status
from campus_lost_found_app.models.user_model import UserCreate
from campus_lost_found_app.models.post_model import PostCreate

app = FastAPI()

mydb = mysql.connector.connect(
    host="centerbeam.proxy.rlwy.net",
    port="16492",
    user="root",
    password="DgUUNjJAkgVFCwSVSUParLhlcLXpSpOL",
    database="railway"
)

@app.get('/')
def root():
    return {
        'message' : 'Welcome to campus beacon'
    }

@app.get("/users")
async def get_users():
    cursor = mydb.cursor(dictionary=True)

    cursor.execute("select * from Users")

    result = cursor.fetchall()

    raw_output = json.dumps(result)

    json_output = json.loads(raw_output)

    cursor.close()

    return json_output

@app.get("/posts")
async def get_posts():
    cursor = mydb.cursor(dictionary=True)

    cursor.execute("select * from Posts")

    result = cursor.fetchall()

    raw_output = json.dumps(result)

    json_output = json.loads(raw_output)

    cursor.close()

    return json_output

@app.post("/users")
async def create_users(user: UserCreate):
    try:
        cursor = mydb.cursor()

        cursor.execute("insert into Users(email, password) values (%s, %s)", (user.email, user.password))

        mydb.commit()

        cursor2 = mydb.cursor(dictionary=True)

        cursor2.execute("select * from Users where email=%s", (user.email,))

        result = cursor2.fetchall()

        raw_output = json.dumps(result[0])

        json_output = json.loads(raw_output)

        cursor.close()
        cursor2.close()

        return json_output
    
    except mysql.connector.errors.IntegrityError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Duplicate email not allowed")


@app.post("/posts")
async def create_posts(post: PostCreate):
    cursor = mydb.cursor()

    cursor.execute('''insert into Posts(
        item_title,
        item_category,
        item_description,
        item_photo,
        campus_building,
        specific_location,
        date,
        uid,
        post_type)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
            [
                post.item_title,
                post.item_category,
                post.item_description,
                post.item_photo,
                post.campus_building,
                post.specific_location,
                post.date,
                post.uid,
                post.post_type
            ]
        )
    
    mydb.commit()
    cursor.close()

    return post


@app.get('/users/{uid}')
async def get_user_by_id(uid: str):
    cursor = mydb.cursor(dictionary=True)

    cursor.execute("select * from Users where uid=%s", [uid.strip()])

    result = cursor.fetchall()

    raw_output = json.dumps(result)

    json_output = json.loads(raw_output)

    cursor.close()

    return json_output

@app.get('/posts/{item_id}')
async def get_post_by_id(item_id: str):
    cursor = mydb.cursor(dictionary=True)
    
    cursor.execute("select * from Posts where item_id=%s", [item_id.strip()])
    
    result = cursor.fetchall()
    
    raw_output = json.dumps(result)
    
    json_output = json.loads(raw_output)

    cursor.close()
    
    return json_output

@app.get('/posts/category/{item_category}')
async def get_post_by_category(item_category: str):
    cursor = mydb.cursor(dictionary=True)

    category = str.capitalize(item_category)

    cursor.execute('select * from Posts where item_category=%s', [category.strip()])

    result = cursor.fetchall()
        
    raw_output = json.dumps(result)
        
    json_output = json.loads(raw_output)

    cursor.close()
        
    return json_output

@app.get('/posts/type/{post_type}')
async def get_post_by_type(post_type: str):
    cursor = mydb.cursor(dictionary=True)

    type = str.capitalize(post_type)

    cursor.execute('select * from Posts where post_type=%s', [type.strip()])

    result = cursor.fetchall()
    
    raw_output = json.dumps(result)
    
    json_output = json.loads(raw_output)

    cursor.close()
    
    return json_output

@app.get('/posts/uid/{uid}')
async def get_posts_by_uid(uid: str):
    cursor = mydb.cursor(dictionary=True)

    cursor.execute('select * from Posts where uid=%s', [uid.strip()])

    result = cursor.fetchall()
    
    raw_output = json.dumps(result)
    
    json_output = json.loads(raw_output)

    cursor.close()
    
    return json_output






































