db.getCollection('engine_model').find({"version" : {$gt: 1}})
db.getCollection('engine_model').find({"version" : {$gt: 1}}).size()

db.getCollection('engine_model').find({}).size();
db.getCollection('engine_model').find({"version" : 1}).size()
db.getCollection('engine_model').distinct("product_index_href").length
db.getCollection('engine_model').find({"product_index_href" : '/m31/7765_index.html'})

db.getCollection('engine_model').aggregate([
  { $group: { 
    _id:"$product_index_href", 
    dups: {$addToSet:'$_id'},
    count: { $sum: 1 } 
  }}, 
  { $match: { 
    count: { $gt: 1 } 
  }}
]).forEach(function(it){
    //print(db.getCollection('engine_model').find({_id: {$in: it.dups}}))
    it.dups.shift();
    db.getCollection('engine_model').remove({_id: {$in: it.dups}});

});
  
db.getCollection('truck_model_new').find({}).size()
db.getCollection('truck_model_new').distinct("model_index_url").length

db.getCollection('truck_model_original').find({})
db.getCollection('truck_model_original').find({}).size()
db.getCollection('truck_model_original').distinct("model_index_url").length
db.getCollection('truck_model').find({"model_index_url": 'https://product.360che.com/s26/6705_63_index.html'})

db.getCollection('truck_model').aggregate([
  { $group: { 
    _id:"$model_index_url", 
    dups: {$addToSet:'$_id'},
    count: { $sum: 1 } 
  }}, 
  { $match: { 
    count: { $gt: 1 } 
  }}
]).forEach(function(it){
    it.dups.shift();
    db.getCollection('truck_model').remove({_id: {$in: it.dups}});

});

db.getCollection('truck_model_x_distinct').find({}).size()
db.getCollection('truck_model_x_distinct').distinct("model_index_url").length
db.getCollection('truck_model_x_distinct').find({"model_index_url": "https://product.360che.com/s26/6660_63_index.html"})
db.getCollection('truck_model_x_distinct').aggregate([
  { $group: { 
    _id:"$model_index_url", 
    dups: {$addToSet:'$_id'},
    count: { $sum: 1 } 
  }}, 
  { $match: { 
    count: { $gt: 1 } 
  }}
]).forEach(function(it){
    it.dups.shift();
    db.getCollection('truck_model_x_distinct').remove({_id: {$in: it.dups}});

});


// engine model


db.getCollection('engine_model').find({})
db.getCollection('engine_model').find({}).size()
db.getCollection('engine_model').distinct("product_index_href").length
db.getCollection('engine_model').find({"model_index_url": "https://product.360che.com/s26/6660_63_index.html"})
db.getCollection('engine_model').aggregate([
  { $group: { 
    _id:"$model_index_url", 
    dups: {$addToSet:'$_id'},
    count: { $sum: 1 } 
  }}, 
  { $match: { 
    count: { $gt: 1 } 
  }}
]).forEach(function(it){
    it.dups.shift();
    db.getCollection('engine_model').remove({_id: {$in: it.dups}});

});

// engine model


db.getCollection('engine_model_detail').find({})
db.getCollection('engine_model_detail').find({}).size()
db.getCollection('engine_model_detail').distinct("发动机厂商：").length
db.getCollection('engine_model_detail').distinct("发动机：").length
db.getCollection('engine_model_detail').find({"发动机：": "CY4SK761"})
db.getCollection('engine_model_detail').find({"发动机：": "CY4SK661"})
db.getCollection('engine_model_detail').aggregate([
  { $group: { 
    _id:"$发动机：", 
    dups: {$addToSet:'$_id'},
    count: { $sum: 1 } 
  }}, 
  { $match: { 
    count: { $gt: 1 } 
  }}
]).forEach(function(it){
    it.dups.shift();
    db.getCollection('engine_model_detail').remove({_id: {$in: it.dups}});

});

 