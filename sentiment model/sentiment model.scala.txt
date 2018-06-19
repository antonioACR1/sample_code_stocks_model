import org.apache.spark.ml.feature.Word2Vec
#for human sentiment classification
val a=DF.select("tweet").collect()
val sentiment=List(2,1,1,1,1,2,2,2,2,2,2,2,1,2,2,2,2,1,0,2,1,2,1,1,1,1,2,0,2,2,2,2,1,1,2,2,1,2,1,1,2,2,2,1,0,2,2,1,2,2,2,2,2,2,2,1,1,2,2,0,1,1,0,2,2,2,0,1,2,2).map(i=>i.asInstanceOf[Double])

val word2Vec = new Word2Vec().setInputCol("filtered").setOutputCol("result").setVectorSize(3).setMinCount(0)
val model = word2Vec.fit(ds)

val dfTweetAsVector = model.transform(ds)

import org.apache.spark.sql.Row
import org.apache.spark.sql.types.{StructField, DoubleType}

val rows = dfTweetAsVector.rdd.zipWithIndex.map(_.swap).join(sc.parallelize(sentiment).zipWithIndex.map(_.swap)).values.map{ case (row: Row, x: Double) => Row.fromSeq(row.toSeq :+ x) }

val myDF=sqlContext.createDataFrame(rows, dfTweetAsVector.schema.add("sentiment", DoubleType, false))

val Array(trainingData, testData) = myDF.randomSplit(Array(0.7, 0.3))


import org.apache.spark.ml.feature.StringIndexer

val labelIndexer = new StringIndexer().setInputCol("sentiment").setOutputCol("indexedSentiment").fit(trainingData)
val training=labelIndexer.transform(trainingData)

import org.apache.spark.ml.classification.RandomForestClassifier
val rf = new RandomForestClassifier().setLabelCol("indexedSentiment").setFeaturesCol("result").setNumTrees(50)
val model = rf.fit(training)

val predictions = model.transform(testData)

val predictionsIndexedLabel=labelIndexer.transform(predictions)

import org.apache.spark.ml.evaluation.MulticlassClassificationEvaluator

val evaluator = new MulticlassClassificationEvaluator().setLabelCol("indexedSentiment").setPredictionCol("prediction")
val accuracy = evaluator.evaluate(predictionsIndexedLabel)


