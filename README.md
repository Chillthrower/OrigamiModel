# Running the Origami App Project

1. Navigate to the Origami App directory:
    ```bash
    cd OrigamiApp
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:
    - For Windows:
        ```bash
        venv\Scripts\Activate
        ```
    - For Linux:
        ```bash
        source venv/bin/activate
        ```

4. Install project dependencies from the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

5. Change to the `image_classification_project` directory:
    ```bash
    cd image_classification_project
    ```

6. Run the project:
    ```bash
    python manage.py runserver
    ```

Now, your Origami App project should be up and running!
