db.getCollection('engine_model').find({"version" : {$gt: 1}})
db.getCollection('engine_model').find({"version" : {$gt: 1}}).size()

db.getCollection('engine_model').find({"version" : 1})
db.getCollection('engine_model').find({"version" : 1}).size()
db.getCollection('engine_model').distinct("product_index_href",{"version" : 1}).length


db.getCollection('truck_model').find({"version" : 1})
db.getCollection('truck_model').find({"version" : 1}).size()

//version change for engine_model
db.getCollection('engine_model').find({}).forEach(
    function(item){
        db.getCollection('engine_model').update({"_id": item._id},{$set:{"version": 1}})
    })
