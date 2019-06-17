REM mongoexport -d truck_catcher_db -c truck_model -o truck_model.dat
REM mongoexport -d truck_catcher_db -c truck_model_detail -o truck_model_detail.dat
REM mongoexport -d truck_catcher_db -c air_filter_detail -o air_filter_detail.dat
REM mongoexport -d truck_catcher_db -c engine_model -o engine_model.dat
REM mongoexport -d truck_catcher_db -c engine_model_detail_new -o engine_model_detail_new.dat


 mongoexport -d truck_parts_cn357_db -c cn357_filter_model_detail -o cn357_filter_model_detail.dat
 mongoexport -d truck_parts_cn357_db -c cn357_truck_model -o cn357_truck_model.dat
 mongoexport -d truck_parts_cn357_db -c cn357_truck_model_detail -o cn357_truck_model_detail.dat
 mongoexport -d truck_parts_cn357_db -c cn357_engine_model -o cn357_engine_model.dat
 mongoexport -d truck_parts_cn357_db -c cn357_engine_model -o cn357_engine_model_detail.dat
 mongoexport -d truck_parts_cn357_db -c error_coll -o error_coll.dat



REM mongoimport -d truck_parts_db -c truck_model truck_model.dat
REM mongoimport -d truck_parts_db -c truck_model_detail_new truck_model_detail.dat
REM mongoimport -d truck_parts_db -c filter_detail air_filter_detail.dat
REM mongoimport -d truck_parts_db -c engine_model engine_model.dat
REM mongoimport -d truck_parts_db -c engine_model_detail_new engine_model_detail_new.dat
REM mongoimport -d truck_parts_db -c filter_model filter_model.dat
REM mongoimport -d truck_parts_db -c filter_model_detail filter_model_detail.dat