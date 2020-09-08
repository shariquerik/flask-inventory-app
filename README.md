> Note: This application is only build for learning and demostration purpose.

# Flask Inventory App

An Inventory Management Web Application built on [Flask](http://flask.pocoo.org/) used to manage inventory of a list of products in respective warehouses. User can move product from one location to another, can only add product to location also can remove from the location.

### Prerequisites

To run this system you will need :

- [Python 3](https://www.python.org/downloads/)


## Development Quickstart

To develop this project:

1.  Clone the repository:

    ```python
    $ git clone https://github.com/shariquerik/flask-inventory-app.git
    $ cd flask-inventory-app-master
    ```

2.  Create a virtual environment:

    ```python
    $ py -m venv env
    ```
    
3.  Activate virtual environemnt:

    *bash*
    
    ```sh
    source env/bin/activate
    ```

    
    *windows*
    ```ps
    $ env\Scripts\activate
    ```
    
4. Install Dependencies:

    ```python
    $ pip install -r requirements.txt
    ```
    
5. Run the application:

    ```python
    $ python run.py
    ```
    
6. Visit [http://localhost:5000/](http://localhost:5000/) from your browser to access the app.
    


## Screenshots:

Below are the screenshots of the views available in application. 

- ### Products:
This view helps to manage products:
![Products page](screenshots/allProducts.png?raw=true "Products View")


- ### Locations:
This view helps to manage Warehouse Locations:
![Locations page](screenshots/allLocation.png?raw=true "Locations View")


- ### Product Movements:
This view helps to make data entry of product movement:
![Product Movements page](screenshots/allMovement.png?raw=true "Movements View")


- ### Dashboard:
This reports shows the balance quantity in each location:
![Dasboard page](screenshots/dashboard.png?raw=true "Dashboard")
