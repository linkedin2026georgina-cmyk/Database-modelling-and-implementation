# NoSQL Database Report: Pollution Data with MongoDB

## Introduction
The standard relational database models are usually good for organised data and defined schemas, but when working with huge, unstructured, or semi-structured datasets, NoSQL databases provide greater flexibility and scalability.
The standard relational database model is ideal for organised data and defined schemas, but when working with huge, unstructured, or semi-structured datasets, NoSQL databases provide greater flexibility and scalability. Component 6 focusses on creating and implementing a NoSQL database model for a specific monitor station in the air quality dataset. MongoDB was chosen to properly format and store the data to query readings based on station identification, timestamps, and pollution levels. In addition, a sample dataset was imported into a mongoDB model, and a practical query was executed to show data retrieval and analysis capabilities in the NoSQL environment.
This component also highlights the advantages of NoSQL systems in handling complex data structures and emphasizes the practical implementation of a query to extract meaningful insights.

### MongoDB
MongoDB's built-in aggregation framework makes difficult data processing jobs easier, such as estimating average pollutant levels, detecting anomalies, and doing time-series analysis. Also its replication and horizontal scaling provide data redundancy and high availability, which is critical for sensor data monitoring and analysis.

## Data Model
The data model is structured as a collection of documents, with each document representing a monitoring station defined by a unique station_id. Each station has metadata such as a name, location, and a readings array. Geospatial coordinates are included in the location object, which allows for easier spatial indexing and queries. The readings array consists of several sensor readings, each of which captures pollutant levels and environmental data at a certain date and time. This nested structure takes advantage of MongoDB's ability to hold complicated data hierarchies in a single document, which reduces the need for joins and improves query efficiency.

The selected station is **Colston Avenue** with `station_id: 501`. This station monitors multiple pollutants including, NOx, PM2.5, CO, and more.


```json
[
  {
    "station_id": 501,
    "name": "Colston Avenue",
    "location": {
      "constituency": "Bristol",
      "geo": {
        "type": "Point",
        "coordinates": [
          -2.5833,
          51.45
        ]
      }
    },
    "readings": [
      {
        "datetime": "2019-04-29T23:00:00Z",
        "nitrogen_oxides": 122.25,
        "nitrogen_dioxide": 49.25,
        "nitric_oxide": 47.75,
        "pm_10": 30.4,
        "ozone_concentration": null,
        "temperature": null,
        "non_vol_pm_10": null,
        "vol_pm_10": null,
        "non_vol_pm_2_5": null,
        "pm_2_5": null,
        "vol_pm_2_5": null,
        "carbon_monoxide": null,
        "relative_humidity": null,
        "air_pressure": null,
        "sulphur_dioxide": null,
        "current": false
      },
      {
        "datetime": "2019-04-30T03:00:00Z",
        "nitrogen_oxides": 42.25,
        "nitrogen_dioxide": 35.25,
        "nitric_oxide": 4.5,
        "pm_10": 20.275,
        "ozone_concentration": null,
        "temperature": null,
        "non_vol_pm_10": null,
        "vol_pm_10": null,
        "non_vol_pm_2_5": null,
        "pm_2_5": null,
        "vol_pm_2_5": null,
        "carbon_monoxide": null,
        "relative_humidity": null,
        "air_pressure": null,
        "sulphur_dioxide": null,
        "current": false
      },// more readings
    ]
  }
]
 ```
### Import process
To manage the dataset more efficiently, the JSON model was imported into MongoDB using the mongoimport function. This command-line allows for easy data transfer from JSON files to MongoDB collections while keeping the hierarchical structure and document-based format. The import process was carried out with the following command:

```
mongoimport --db pollution --collection stations --file station.json

```
### Query

The first aggregation pipeline extracts station 501's highest nitrogen oxides measurement. It starts with a "match" stage, which filters documents to include only those with station_id 501. The "unwind" stage then deconstructs the readings array, converting each reading into its document in the pipeline.
The "sort" stage then sorts these individual readings in descending order using the readings.nitrogen_oxides field, ensuring that the largest value appears first. By specifying "limit: 1"", the pipeline retains only the top reading. Finally, the "project" stage reshapes the output to include just the datetime and the nitrogen_oxides value of that reading. This sequence efficiently retrieves the timestamped peak nitrogen oxide concentration while reducing data transfer and computation on the application side.

```
db.stations.aggregate([
  { $match: { "station_id": 501 } }, 
  { $unwind: "$readings" },
  { $sort: { "readings.nitrogen_oxides": -1 } }, 
  { $limit: 1 }, 
  { $project: { 
      "datetime": "$readings.datetime",
      "nitrogen_oxides": "$readings.nitrogen_oxides"
  }}
])
```

The second pipeline estimates the daily average PM10 levels at Station 501. After the initial "match" stage filters for station_id: 501 and the "unwind" stage separates each element of the readings array, a "project" stage converts each reading's datetime string into a Date object using "toDate" and formats it as YYYY-MM-DD using "dateToString", labelling this field date. It also extracts the PM_10 value. The "group" step then aggregates these documents based on the formatted date, calculating the average pm_10 for each day using the avg_pm_10 column.
Finally, "sort" sorts the resultant daily averages in ascending date order (_id=1). This pipeline provides a simple, chronological representation of daily mean PM10 values from within MongoDB, taking advantage of the aggregation framework for rapid time-series analysis.

```
db.stations.aggregate([
  { $match: { "station_id": 501 } },
  { $unwind: "$readings" },
  { $project: {
      date: {
        $dateToString: {
          format: "%Y-%m-%d",
          date: { $toDate: "$readings.datetime" }
        }
      },
      pm_10: "$readings.pm_10"
  }},
  { $group: {
      date: "$date",
      avg_pm_10: { $avg: "$pm_10" },
  }},
  { $sort: { _id: 1 } }
])
```
A screen capture of the results of these queries is in the submission folder.

### conclusion
This component showcased the complete design, construction, and querying of a NoSQL database dedicated to a sample dataset used in the previous components.Mongoimport was used to import the JSON-based data model into MongoDB.
Finally, two aggregation pipelines were created : one to extract the highest nitrogen oxide reading and another to compute daily average PM₁₀ levels. These queries demonstrated MongoDB's ability to effectively unwind nested arrays, convert and format dates, group and aggregate time-series data, and project only the required features.   These methods demonstrate the benefits of NoSQL for managing real-time environmental data, providing both flexibility and performance for advanced analysis. 




