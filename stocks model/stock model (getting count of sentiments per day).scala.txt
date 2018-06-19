val distinctDates=sc.parallelize(myDF.select("fecha").collect().distinct).flatMap(_.toSeq).map(i=>i.asInstanceOf[java.sql.Date]).collect()


val trainInitialDate="2018-05-29"

val trainLastDate="2018-06-04"

val testInitialDate="2018-06-05"

val testFinalDate="2018-06-07"

val trainPeriod=myDF.filter(col("fecha")<=trainLastDate && col("fecha")>=trainInitialDate)


import org.apache.spark.sql.functions.countDistinct
var DFs=List[org.apache.spark.sql.DataFrame]()
for(i<-distinctDates){
val tempTrain=trainPeriod.filter(col("fecha")===i)
val tempPrediction=model.transform(tempTrain)
val tempObservation=tempPrediction.groupBy("prediction").count()
val names=Seq("prediction","count"+i)
val tempObservationRenamed=tempObservation.toDF(names:_*).cache()
DFs=DFs:+tempObservationRenamed
}

var dfJoined=Seq((1.0,0.0),(0.0,0.0),(2.0,0.0)).toDF("prediction","dummy")
for(i<-0 to DFs.size-1){
dfJoined=dfJoined.join(DFs(i),Seq("prediction"),"left_outer")}

dfJoined=dfJoined.drop("dummy").na.fill(0)

dfJoined.coalesce(1).write.format("com.databricks.spark.csv").option("header","true").save("/user/cloudera/dfJoined.csv")

