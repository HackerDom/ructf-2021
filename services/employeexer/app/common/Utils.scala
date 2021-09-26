package common

import java.security.MessageDigest
import java.util.Base64

object Utils {
  def baseHash(source: String): String = Base64.getEncoder.encodeToString(MessageDigest.getInstance("MD5").digest(source.getBytes))
}
