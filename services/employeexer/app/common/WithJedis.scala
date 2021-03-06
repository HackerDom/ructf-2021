package common

import redis.clients.jedis.{Jedis, JedisPool, Transaction}


class WithJedisException(val innerException: Throwable, message: String) extends Exception(message)


class WithJedis(private val jedisPool: JedisPool) {
  def withJedis[T](block: (Jedis) => T): T = {
    var jedisForClose: Option[Jedis] = None
    try {
      val jedis = jedisPool.getResource
      jedisForClose = Some(jedis)
      block(jedis)
    } catch {
      case e: Throwable => e.printStackTrace()
        throw new WithJedisException(e, s"Error during jedis operation: ${e.getMessage}")
    } finally {
      jedisForClose match {
        case Some(value) => value.close()
        case None =>
      }
    }
  }
  def withJedisTransaction[A, B](keys: Seq[String], reading: (Jedis) => A, updating: (A, Transaction) => B): Unit = withJedis { jedis =>
    jedis.watch(keys:_*)
    val readingResult = reading(jedis)
    val transaction = jedis.multi()
    updating(readingResult, transaction)
    transaction.exec()
    jedis.unwatch()
  }
}
