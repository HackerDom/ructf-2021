package common

import org.request.{Employee, StrippedEmployee}

import java.security.MessageDigest
import java.util.Base64

object Utils {
  def baseHash(source: String): String = Base64.getEncoder.encodeToString(MessageDigest.getInstance("MD5").digest(source.getBytes))

  def stripEmployee(employee: Employee): StrippedEmployee =
    new StrippedEmployee(employee.id, employee.owner, employee.employee.name, employee.employee.description, employee.employee.tags)
}
