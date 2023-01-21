<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="">
    <img src="assets/Smartathon.jpg" width=90% alt="💻 Logo">
  </a>
<br>
<br>
  <h1 align="center">Pothole severity classification via computer vision</h1>

The work of an artificial intelligence technology that reads letters and numbers and accordingly the plate is classified according to specific criteria and standards, to raise the quality of classifying plates to a digital system, which facilitates the management of auctions and sales are carried out at deliberate prices

<br>

<!-- GETTING STARTED -->
## Getting Started 

To run this project you will need to some steps to get things to work.

### Prerequisites

First we will need download all the libraries that we will need for this project. You could do that by runing these snippets of code. 
* Creating new envierment
    ```sh
    conda create -n sklearn-env -c conda-forge scikit-learn
    conda activate sklearn-env
    ```
* Install libraries
  ```sh
  # conda create --name sklearn-env --file requirements.txt
  pip3 install flask
  pip3 install convert_numbers
  pip3 install pandas
  ```
  <p align="right">(<a href="#top">back to top</a>)</p> 

### Generate Data
Since the data is not been provided by the organizing committee we had to be creative and generate the data by ourselfs. To run the code for the data generator you will need to run this command.
  ```sh
  # python3 ./code/generate_data.py
  python3 code/data_generator.py
  ```
  <p align="right">(<a href="#top">back to top</a>)</p> 

### Train the Model
Now to the main part of the challenge is creating the AI. To create the models for predicting the plates prices, run these to commands:
  ```sh
  python3 code/letters_model.py
  python3 code/numbers_model.py
  ```
  <p align="right">(<a href="#top">back to top</a>)</p> 

### Run the Website
After applying all the previeus steps now you could try the AI by running the demo website provided in this project. All what you need to do is running this command:
  ```sh
  python3 ./app/app.py
  ```
You will then recive in the terminal the url for the server, in my case it was in `http://127.0.0.1:5000/`
```sh
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
```
Example of what you will see when visit the link:

![sample image](assets/sample.png)

show case example:

<p align="center">
  <img width=100% src="assets/sample.gif" />
</p>


<p align="right">(<a href="#top">back to top</a>)</p> 

### Acknowledgments
- [**Dr. Saud Al-Otaibi**](https://www.linkedin.com/)
- [**Dr. Abdul Rahman Al-Rubaian**](https://www.linkedin.com/)
- [**Dr. Sultan Al-Zahrani**](https://www.linkedin.com/)

<p align="right">(<a href="#top">back to top</a>)</p> 
 
