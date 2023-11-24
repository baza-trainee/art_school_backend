from src.database import get_async_session
from src.auth.utils import create_user

from src.auth.utils import create_user
from src.config import (
    ADMIN_PASSWORD,
    ADMIN_USERNAME,
    CONTACTS,
    DEPARTMENTS,
    SUB_DEPARTMENTS,
)
from src.contacts.utils import create_contacts
from src.database import get_async_session
from src.departments.utils import create_main_departments, create_sub_departments
from src.slider_main.utils import create_slide


async def customlifespan():
    print("lifespan start")
    session = get_async_session()
    async for s in session:
        async with s.begin():
            await create_user(email=ADMIN_USERNAME, password=ADMIN_PASSWORD)
            await create_main_departments(DEPARTMENTS)
            await create_sub_departments(SUB_DEPARTMENTS)
            await create_contacts(**CONTACTS)
            await create_contacts(**CONTACTS)
            await create_slide(title="Slide1", description="Slide1 Test description")
            await create_slide(title="Slide2", description="Slide2 Test description")
            await create_slide(title="Slide3", description="Slide3 Test description")
            await create_slide(title="Slide4", description="Slide4 Test description")
            await create_slide(title="Slide5", description="Slide5 Test description")

    print("lifespan end")


from src.main import app

from fastapi import __version__
from fastapi.responses import HTMLResponse


html = (
    """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FastAPI on Vercel</title>
    <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f8f9fa; /* Light gray background */
        }

        .container {
            background-color: #ffffff; /* White container background */
            padding: 40px; /* Increased padding for a larger container */
            border-radius: 12px; /* Rounded corners */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        h1 {
            color: #343a40; /* Dark gray text */
            font-size: 32px; /* Increased font size */
        }

        ul {
            list-style-type: none;
            padding: 0;
        }

        li {
            margin: 15px 0; /* Increased margin */
        }

        a {
            color: #007bff; /* Business blue link color */
            text-decoration: none;
        }

        p {
            color: #6c757d; /* Medium gray text */
        }
    </style>"""
    + f"""
</head>
<body>
    <div class="container">
        <h1>Hello from FastAPI@{__version__} app</h1>
        <h3>Let's get started?</h3>
        <ul>
            <li><h2><a href="/docs">/docs</a></h2></li>
            <li><h2><a href="/redoc">/redoc</a></h2></li>
        </ul>
        <p>:)</p>
    </div>
</body>
</html>
"""
)


@app.get("/", include_in_schema=False)
async def root():
    return HTMLResponse(html)
