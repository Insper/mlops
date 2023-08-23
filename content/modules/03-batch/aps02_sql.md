# APS 02

In this assignment, we are going to create a new version of the work from the [last class (Click!)](practicing.md).

!!! info "What will change?!"
    All data will be read and written from PostgreSQL.

## Before starting

### Accept assignment

All assignments delivery will be made using Git repositories. Access the link below to accept the invitation and start working on the second assignment.

[Invitation link](https://classroom.github.com/a/L0W-9jWI){ .ah-button }

## Configure assignment repository

You must ensure that the repository has the required folder structure. Create by hand or use your template and then link to the assignment repository.

![](folder_structure.png)

## TASK 0: Create analytical table

In DBeaver, try to create a *SQL query* that performs the necessary transformations in the data of the `item_sale` table, so that they are grouped and with the necessary fields for *model training*, as in the last class.

|      |   store_id |   total_sales |   year |   month |   day |   weekday |
|-----:|-----------:|--------------:|-------:|--------:|------:|----------:|
|    0 |       5000 |      62895.6  |   2023 |       1 |     1 |         6 |
|    1 |       5000 |      42351.1  |   2023 |       1 |     2 |         0 |
...
| 1636 |       5005 |      46246.3  |   2023 |       9 |    29 |         4 |

!!! tip "Tip!"
    Start with a simple query like:

    ```sql
    SELECT
        store_id,
        client_id,
        product_id,
        date_sale,
        price
    FROM sales.item_sale;
    ```

    Then make the necessary adjustments.

!!! tip "Tip!"
    At first, use **fixed dates**, for example, assuming your model will use data from `2023-06-01` to `2023-06-30`.

!!! attention
    Notice that the query must do all necessary transformations on the data.

!!! exercise "Question"
    The current day (today) will not have reliable base sales as they are still being made by customers. Adjust your query so that the data is:

    - From the day before today
    - Up to a `delta` in the past. Choose your `delta`, for example one years.

!!! danger "Important!"
    Now "today" cannot be fixed in the query anymore, google for `CURRENT_DATE` + postgres and make the necessary adjustments!

## TASK 1: Query file for analytical table

We will no longer have *CSV* in the `data` folder!

!!! exercise "Question"
    Create an `.env` file with the database access credentials.


!!! exercise "Question"
    Create a `data/train.sql` file containing the query from the previous task.

!!! exercise "Question"
    Change your program so that:

    - The `data/train.sql` file is read as text.
    - Database credencials are loaded from `.env` file.
    - Text query is executed to return a Pandas DataFrame in the model retraining step.

!!! info
    Search how to:

    - Create a PostgreSQL database connection in Python.
    - How to read a Pandas DataFrame from a query and connection.

!!! warning "For now..."
    For now, keep saving and reading the model in the `models` folder!

!!! exercise text long "Question"
    Why should we avoid using `*` in production queries?
    
    Explain why making queries like this one is a bad practice:

    ```sql
    SELECT * FROM som_table
    ```

## TASK 2: Exporting predictions

The way data predicted by the model are saved depends a lot on how the model is used.

In this activity, let's assume that:

- The model always makes predictions from the current day to the next six days.
- The predictions are stored in another `schema` called `sales_analytics`.
- Old predictions are not stored. Whichever prediction script is run, the table that stores predictions should be cleared and only the predictions for the day through the next week should be kept in the table.

!!! bug "Challenge"
    Try to create a query that generates a table with all the days and fields needed for prediction:

    ![](predict_dates.png)

    Then, save these lines in a new table `"scoring_ml_YOUR_INSPER_USERNAME"` on schema `sales_analytics`. In Python, iterate over these records calling and storing your model's predictions!

    Remember to delete old records from this table every time you make predictions.

!!! exercise "Question"
    Change your prediction code to meet the requested requirements.


## TASK 3: A new View!

Let's pass the code from `data/train.sql` to a view on the database.

!!! exercise "Question"
    Create a view with the contents of `data/train.sql`. The view can be called `view_abt_train_YOUR_INSPER_USERNAME` an be on schema `sales_analytics`.

!!! exercise "Question"
    Change the query in `data/train.sql` to query the newly created view.

    DO NOT use `"SELECT *"`!!!

Submit the activity by the [**deadline**](../../deadlines.md)!