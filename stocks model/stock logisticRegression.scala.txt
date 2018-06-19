/*hdfs dfs -copyToLocal /user/cloudera/dfJoined.csv /home/cloudera/Downloads/stocks_model/stocks_model

proceed to py file, then put the resulting file into hdfs

hdfs dfs -put /home/cloudera/Downloads/stocks_model/stocks_model/data/stockDF.csv /user/cloudera/stockDF.csv */



import org.apache.spark.ml.classification.LogisticRegression
val sqlContext=new org.apache.spark.sql.SQLContext(sc)
import sqlContext.implicits._
import org.apache.spark.sql.types.DoubleType
import org.apache.spark.ml.feature.VectorAssembler
import org.apache.spark.ml.feature.StringIndexer
import org.apache.spark.ml.evaluation.MulticlassClassificationEvaluator

val df=sqlContext.read.format("com.databricks.spark.csv").option("header","true").option("delimiter",",").option("inferSchema","true").load("/user/cloudera/stockDF.csv")

val dfDoubles=df.withColumn("DoubleSentiment1",df("sentiment1").cast(DoubleType)).withColumn("DoubleSentiment2",df("sentiment2").cast(DoubleType)).withColumn("DoubleSentiment3",df("sentiment3").cast(DoubleType))

val assembler=new VectorAssembler().setInputCols(Array("DoubleSentiment1","DoubleSentiment2","DoubleSentiment3")).setOutputCol("features")

val dfAssembled=assembler.transform(dfDoubles)

val Array(trainingData, testData) = dfAssembled.randomSplit(Array(0.6, 0.4))

val labelIndexer = new StringIndexer().setInputCol("status").setOutputCol("indexedStatus").fit(trainingData)
val training=labelIndexer.transform(trainingData)

val lr = new LogisticRegression().setMaxIter(100).setRegParam(0.01).setElasticNetParam(0.5).setFeaturesCol("features").setLabelCol("indexedStatus")
val model=lr.fit(training)


val testing=labelIndexer.transform(testData)

val predictions=model.transform(testing)

val evaluator = new MulticlassClassificationEvaluator().setLabelCol("indexedStatus").setPredictionCol("prediction")
val accuracy = evaluator.evaluate(predictions)

