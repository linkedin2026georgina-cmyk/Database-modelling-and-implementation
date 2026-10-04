//query 1
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

//query 2
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
