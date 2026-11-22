from pydantic import BaseModel

class PostCreate(BaseModel):
    item_title: str
    item_category: str
    item_description: str
    item_photo: str
    campus_building: str
    specific_location: str
    date: str
    uid: str
    post_type: str