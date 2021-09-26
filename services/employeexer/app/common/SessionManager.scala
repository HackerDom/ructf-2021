package common

import redis.clients.jedis.JedisPool

import scala.util.Random


class SessionManager(private val jedisPool: JedisPool) extends WithJedis(jedisPool) {
  def create(username: String): String = {
    println(s"Create session for $username")
    val salt = "salt:" + Random.alphanumeric.take(32).mkString("")
    println(salt)
    val secret = Utils.baseHash(username + salt)
    println(secret)

    withJedis { jedis =>
      jedis.set(username, salt)
    }
    secret
  }

  def delete(username: String): Unit ={
    try {
      withJedis { jedis =>
        jedis.del(username)
      }
    } catch {
      case _: Throwable =>
    }
  }

  def validate(username: String, secret: String): Boolean = {
    withJedis { jedis =>
      val salt = jedis.get(username)
      Utils.baseHash(username + salt) == secret
    }
  }
}
