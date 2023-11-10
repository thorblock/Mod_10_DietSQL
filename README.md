# Mod_10_DietSQL
Using Python and SQLAlchemy ORM to do a basic climate analysis and data exploration of your climate database. 

# Resources Folder
The `Resources` folder serves as a repository for essential data files. Both `Jupyter_Surf` and `Flask_Surf` files make use of the included SQLite file. Additionally, CSV files are provided for an initial data review, offering insights into potential references that can be extracted.

# Jupyter_Surf
The `Jupyter_Surf` module consists of a Jupyter notebook designed for in-depth analysis of Hawaii's Surfs Up data. Leveraging SQLAlchemy as our guide to Object-Relational Mapping (ORM).

# Flask_Surf
This project is centered around a Flask API that handles various paths, each serving specific functionalities. The date range path has been a source of complexity, and detailed instructions have been added to guide users.

## Path Outputs
The majority of path outputs are designed to utilize JSON-formatted dictionaries, providing a structured and readable response. This format is preferred over 1D lists, as it enhances clarity and organization.

### Station Path Exception
An exception to this pattern is observed in the station path. Here, the `.ravel` method is employed to create a 1D list of stations. This approach is chosen because there is only one value required to define the stations themselves. While it deviates from the dictionary format, it makes sense in this context.

## User Consideration
To ensure a smooth experience for all users, please follow the provided instructions for the date range path. Let's avoid becoming the user who overlooks these guidelines, as it can lead to unexpected issues.

