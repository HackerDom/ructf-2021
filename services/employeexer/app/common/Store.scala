package common

import java.io.FileOutputStream
import java.nio.file.{Files, Path}
import java.util.Base64
import scala.collection.mutable
import scala.jdk.CollectionConverters.IteratorHasAsScala
import scala.util.Using

class StoreException(message: String) extends Exception(message)


class Store(private val path: Path) extends mutable.Map[String, Array[Byte]] {
  if (Files.exists(path)) {
    if (!Files.isDirectory(path)) {
      throw new StoreException("Path '" + path.toString + "' is exists and it is not a directory")
    }
  } else {
    Files.createDirectories(path)
  }
  val shortDir: Path = path.resolve("short")
  if (!shortDir.toFile.exists()) {
    Files.createDirectory(shortDir)
  }

  private def getFilePath(key: String, encodeKey: Boolean = true, createSubdir: Boolean = false) = {
    val preparedKey = if (encodeKey) Base64.getEncoder.encodeToString(key.getBytes) else key

    if (preparedKey.length < 3) path.resolve("short").resolve(preparedKey)
    else {
      val prefix = preparedKey.substring(0, 2)
      val prefixDir = path.resolve(prefix)
      if (createSubdir && !prefixDir.toFile.exists()) {
        Files.createDirectory(prefixDir)
      }
      prefixDir.resolve(preparedKey)
    }
  }

  private def get(key: String, encodeKey: Boolean): Option[Array[Byte]] = {
    val filePath = getFilePath(key, encodeKey)

    if (filePath.toFile.exists()) {
      val res = Files.readAllBytes(filePath)
      Some(res)
    } else None
  }

  override def get(key: String): Option[Array[Byte]] = get(key, encodeKey = true)

  override def addOne(elem: (String, Array[Byte])): Store.this.type = {
    val filePath = getFilePath(elem._1, createSubdir = true)
    Using(new FileOutputStream(filePath.toString)) { file =>
      file.write(elem._2)
    }
    this
  }

  override def iterator: Iterator[(String, Array[Byte])] =
    Files.walk(path).iterator().asScala.filter(Files.isRegularFile(_)).map { file =>
      file.getFileName.toString -> this.get(file.getFileName.toString, encodeKey = false).get
    }

  override def subtractOne(elem: String): Store.this.type = {
    this
  }
}
