## Gungnir - [GrapeNews](ucdgrapenews.com)

### Files Structure:

* gungnir/
* --gungnir/ (Root APP)
* --dataCollector/ (APP-1 data collector and processor)
* --gungnirRest/ (APP-2 RESTful APIs)
* --accounts/ (Store and process user information)
* --frontend/
* --static/ (Store static files for front end)
* --django_logging_files/ (Store logging files)
* --Documentations/ (Code's documentations)
* ---- Deploy_Manual_Windows.pdf
* ---- Deploy_Manul_Ubuntu1604.pdf
* --requirements.txt (System dependencies)
* --Init_data_collector.py (Initial data collecting script)
* --Clustering_news_filter.py (Independent clustering script)
* --model_test.py (Database testing script)
* --user_info_test.py
* --mock_data.py (Mock data for the front end)
* --mock_unit_test.py (Mock unit test file)
* --manage.py



### Installation
    * Install python-3.x
    
    * Install postgresSql
    
    * Install celery dependencies

    * Install Node.js
    
    
## Quick Start:
### Backend Build Setup:
``` bash
#  Install dependencies:
pip install -r requirements.txt

# Create migrations for those changes:
python manage.py makemigrations

# Apply those changes to the database:
python manage.py migrate

# Clean the datebase:
python manage.py flush

# Set independent Django running environment:(Only for Windows)
set DJANGO_SETTINGS_MODULE=gungnir.settings

# Initialized data collection:
python Init_data_collector.py

# Run Django server:
python manage.py runserver
```

### Frontend Build Setup:
``` bash
# under /frontend  
# install dependencies from package.json
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```

For detailed explanation on how front-end works, checkout the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).

> Timeline visualization - [TimelineJS3](https://github.com/NUKnightLab/TimelineJS3)

## Production Deployment:
If you want to deploy this website online, please follow the next manuals.
* For Windows, please refer **Documentations/Deploy_Manual_Windows.pdf**
* For Ubuntu, please refer **Documentations/Deploy_Manul_Ubuntu1604.pdf**

##### Contributors:
* Wenrui Shen <wenrui.Shen@ucdconnect.ie>
* Xinlei Lin <xinlei.lin@ucdconnect.ie>
* Zhenyu Liu <zhenyu.liu@ucdconnect.ie>
* Hong Su <hong.su@ucdconnect.ie>
* Lu Tong <lu.tong@ucdconnect.ie>
* Chang Liu <chang.liu1@ucdconnect.ie>
