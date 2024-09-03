The title of this capstone is Dranks For you.

Overview: This capstone application is designed as a sales point system, primarily focused on managing and processing orders for beverages. It allows users to browse, select, and order drinks, with a structured backend to handle user management, order processing, and inventory tracking of beverages, liquors, and ingredients.

Components:

User Management:

The application includes a user table that stores user-related data such as username, email, name, and a boolean admin field to differentiate between regular users and administrators.
Each user is uniquely identified by an id and a uid (user identifier).

Beverage Catalog:

The beverage table holds the details of each beverage, including its name, description, price, and associations with specific liquors and ingredients.
The table references the liquor and ingredients tables to ensure that each beverage can be accurately described in terms of its components.

Order Processing:

The order table tracks individual orders placed by users, including the total order amount and the payment type.
The orderbeverages table acts as a junction table that links each order to the beverages it contains, facilitating a many-to-many relationship between orders and beverages.

Liquor and Ingredients Inventory:

The liquor and ingredients tables maintain a list of all available liquors and ingredients, respectively. These are essential for constructing the beverages offered in the application.

Relationships:

The application uses foreign key relationships to ensure data integrity. For instance, each beverage is associated with a specific liquor and ingredient, and each order is linked to a user and the beverages included in the order.

The Features that are available on this app:
Admin view
a view of orders
liquors and ingredients names
Bevearges with details and price. \

Link to ERD: https://dbdiagram.io/d/Capstone-Final-66ae3d9c8b4bb5230e2116dc

Link to board

https://www.figma.com/board/NkSvpF2lEvmh45oiQvUDRB/DRANKS?node-id=0-1&node-type=CANVAS&t=oFFc0dKlXBVrn6BY-0



Postman documentation for API 

https://documenter.getpostman.com/view/24380795/2sA3sAhnpk

Loom video

https://www.loom.com/share/d149e0593b0d475d9b0ccf3f8b9d7a90
