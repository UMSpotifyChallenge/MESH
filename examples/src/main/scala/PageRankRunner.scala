/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package umn.dcsg.examples

import scala.io.Source
import dcsg.hg.Util._
import dcsg.hg.{CSV, HyperGraph}
import org.apache.spark.graphx.PartitionStrategy._

object PageRankRunner {
  def main(args: Array[String]): Unit = {

    val logger = Logger("PageRankRunner")

    if (args.size != 7) {
      usage()
      println(args(0))
      System.exit(1)
    }

    val inputfile = args(0)
    val startingIdFile = args(1)
    val fileArg = args(2).toInt

    val numIters = args(3).toInt

    var partitionStrategy = args(4) match {
      case "1D-src" => EdgePartition1D
      case "1D-dst" => EdgePartition1DByDst
      case "2D" => EdgePartition2D
      case "GreedySrc" => GreedySrc
      case "GreedyDst" => GreedyDst
      case "HybridSrc" => HybridSrc
      case "HybridDst" => HybridDst
    }

    val numPartitions = args(5).toInt
    val threshold = args(6).toInt
    val partition = Some(partitionStrategy -> (numPartitions, threshold))

    implicit val sc = makeSparkContext("PageRankRunner")
    try {
      val start1 = System.currentTimeMillis()
      val hg = CSV.hypergraph(inputfile, fileArg)
      val graph = hg.toGraph { case (c, w) => w.toDouble / c } (_ + _)
      val end1 = System.currentTimeMillis()
      val partitionTime = end1 - start1
      logger.log(s"Time taken for partitioning: $partitionTime ms")
      val playlistTracks = Source.fromFile(startingIdFile).getLines.toList.map((s: String) => s.toInt)
      val numIds: Int = playlistTracks.size / 3
      val (startingIds, remainder) = playlistTracks.splitAt(2*numIds)
      logger.log(s"Starting Ids: $startingIds. Remainder Ids: $remainder")
      logger.log("Start Page Rank")

      val start2 = System.currentTimeMillis()
      val prhg = PageRank.prGraph(graph, numIters, startingIds)
      val end2 = System.currentTimeMillis()
      val executionTime = end2 - start2
      logger.log(s"Time taken for Page Rank: $executionTime ms")

    }
    finally {
      sc.stop()
    }
  }

  def usage(): Unit = {
    println("usage: PageRankRuner inputfile startingIdFile fileArg numIters partitionStrategy numPartitions threshold")
  }
}
