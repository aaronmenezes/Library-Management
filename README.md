# Library Mangement  

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)
> https://aaronmenezes.github.io/Library-Mangement-Webapp


>Library-Mangement, is a book library managment service.
Built with Flask, deployed on Heroku. 

## Features

- Perform general CRUD operations on Books and Members
- Issue a book to a member
- Issue a book return from a member
- Search for a book by name and author
- Charge a rent fee on book returns
- Import books into the system using the Book API services and create book records.
- Reports Most popular books with quantity available in the library and total quantity.
- Reports Highest paying Customers.

## Database schema

<img src="https://github.com/aaronmenezes/Library-Mangement-Webapp/blob/main/screens_shots/db_schema.png" width="800" height="450">

## Installation

Library Managment requires [Python 3.7.0](https://www.python.org/downloads/release/python-370/) + to run.

Install the dependencies and start the server.

```sh
cd Library-Mangement
pip install -r requirements.txt
python LibraryService.py
```
