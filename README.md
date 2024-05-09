# My Dash App

This is a Dash application that renders a skills tree based on the data provided in the `skills_tree.json` file.

## Project Structure

The project has the following files and directories:

- `app/main.py`: This file is the entry point of the Dash application. It sets up the Dash app, defines the layout using the `layouts/index.py` file, and registers the callbacks defined in the `callbacks/index.py` file.

- `app/layouts/index.py`: This file exports a function `get_layout` that defines the layout of the Dash application. It uses the data from the `data/skills_tree.json` file to render the skills tree.

- `app/callbacks/index.py`: This file exports functions that define the callbacks for the Dash application. These callbacks handle user interactions and update the visualizations based on the selected data.

- `app/data/skills_tree.json`: This file contains the data for the skills tree. It is a JSON file that defines the structure and hierarchy of the skills.

- `.env`: This file is used to store environment variables for the project. It may contain configuration settings specific to the project.

- `requirements.txt`: This file lists the Python dependencies required for the project. It is used by package managers like pip to install the necessary packages.

## Getting Started

To run the Dash application, follow these steps:

1. Clone the repository to your local machine.

2. Install the required dependencies by running the following command:

   ```
   pip install -r requirements.txt
   ```

3. Set up the environment variables by creating a `.env` file and specifying any necessary configuration settings.

4. Run the Dash application by executing the following command:

   ```
   python app/main.py
   ```

5. Open your web browser and navigate to `http://localhost:8050` to view the skills tree.

## Additional Information

For more details about the project and its implementation, please refer to the source code and comments in the respective files.

Feel free to customize the skills tree data in the `skills_tree.json` file to match your specific requirements.

## License

This project is licensed under the [MIT License](LICENSE).