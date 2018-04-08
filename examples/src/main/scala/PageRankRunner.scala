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

import dcsg.hg.Util._
import dcsg.hg.{CSV, HyperGraph}
import org.apache.spark.graphx.PartitionStrategy._

object PageRankRunner {
  def main(args: Array[String]): Unit = {

    val logger = Logger("PageRankRunner")

    if (args.size != 3) {
      usage()
      println(args(0))
      System.exit(1)
    }

    val inputfile = args(0)
    val fileArg = args(1).toInt

    val numIters = args(2).toInt

    val algorithm: HyperGraph[_, (Int, Int)] => Unit = PageRank.pr(_, numIters)

    implicit val sc = makeSparkContext("PageRankRunner")
    try {
      val start1 = System.currentTimeMillis()
      val hg = CSV.hypergraph(inputfile, fileArg)
      val end1 = System.currentTimeMillis()
      val partitionTime = end1 - start1
      logger.log("Start Page Rank")
      logger.log(s"Time taken for partitioning: $partitionTime ms")

      val start2 = System.currentTimeMillis()
      algorithm(hg)
      val end2 = System.currentTimeMillis()
      val executionTime = end2 - start2
      logger.log(s"Time taken for Page Rank: $executionTime ms")

    }
    finally {
      sc.stop()
    }
  }

  def usage(): Unit = {
    println("usage: PageRankRuner inputfile fileArg numIters")
  }
}
