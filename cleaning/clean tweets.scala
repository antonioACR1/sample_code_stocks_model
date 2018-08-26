/*spark-shell --packages com.databricks:spark-csv_2.10:1.5.0*/

val sqlContext=new org.apache.spark.sql.SQLContext(sc)
import sqlContext.implicits._
val df=sqlContext.read.format("com.databricks.spark.csv").option("header","true").option("delimiter",",").option("inferSchema","true").load("/user/cloudera/tweetsVolaris.csv")


import org.apache.spark.ml.feature.Tokenizer
import org.apache.spark.sql.functions.regexp_replace
import scala.util.matching.Regex

val dfHashesRemoved=df.withColumn("tweet",regexp_replace(df.col("tweet"),"#",""))

val dfRawTextSymbolRemoved1=dfHashesRemoved.withColumn("tweet",regexp_replace(dfHashesRemoved.col("tweet"),"b'",""))

val dfRawTextSymbolRemoved2=dfRawTextSymbolRemoved1.withColumn("tweet",regexp_replace(dfRawTextSymbolRemoved1.col("tweet"),"""b"""",""))

val dfUsernamesRemoved=dfRawTextSymbolRemoved2.withColumn("tweet",regexp_replace(dfRawTextSymbolRemoved2.col("tweet"),"@([A-Za-z]+[A-Za-z0-9-_]+)","USER"))

val dfA=dfUsernamesRemoved.withColumn("tweet",regexp_replace(dfUsernamesRemoved.col("tweet"),"""\\xc3\\xa1""","a"))
val dfE=dfA.withColumn("tweet",regexp_replace(dfA.col("tweet"),"""\\xc3\\xa9""","e"))
val dfI=dfE.withColumn("tweet",regexp_replace(dfE.col("tweet"),"""\\xc3\\xad""","i"))
val dfO=dfI.withColumn("tweet",regexp_replace(dfI.col("tweet"),"""\\xc3\\xb3""","o"))
val dfU=dfO.withColumn("tweet",regexp_replace(dfO.col("tweet"),"""\\xc3\\xba""","u"))

val dfDots=dfU.withColumn("tweet",regexp_replace(dfU.col("tweet"),"""\\xe2\\x80\\xa6""","..."))
val dfN=dfDots.withColumn("tweet",regexp_replace(dfDots.col("tweet"),"""\\xc3\\xb1""","n"))

val dfCapE=dfN.withColumn("tweet",regexp_replace(dfN.col("tweet"),"""\\xc3\\x89""","E"))

val dfSp=dfCapE.withColumn("tweet",regexp_replace(dfCapE.col("tweet"),"""\\n"""," "))

val dfUrl=dfSp.withColumn("tweet",regexp_replace(dfSp.col("tweet"),"""(https|ftp)://(.*)\.([a-z]+)(.*)""","URL"))

val dfX=dfUrl.withColumn("tweet",regexp_replace(dfUrl.col("tweet"),"""\\(.*)""",""))

val dfLower=dfX.withColumn("tweet",lower(col("tweet")))

val dfCleaned=dfLower

import org.apache.spark.sql.types.DateType

val DF = dfCleaned.withColumn("fecha", dfCleaned("fecha").cast(DateType)).distinct

val tokenizer=new Tokenizer().setInputCol("tweet").setOutputCol("words")
val tokenized=tokenizer.transform(DF)

import org.apache.spark.ml.feature.StopWordsRemover

val remover = new StopWordsRemover().setInputCol("words").setOutputCol("filtered")

val ds=remover.transform(tokenized)


