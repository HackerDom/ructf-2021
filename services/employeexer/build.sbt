
name := """employeexer"""
organization := "ru.hackerdom"

version := "1.0-SNAPSHOT"

lazy val root = (project in file(".")).enablePlugins(PlayScala)

scalaVersion := "2.13.6"

libraryDependencies += guice
libraryDependencies += "org.scalatestplus.play" %% "scalatestplus-play" % "5.0.0" % Test
libraryDependencies += "com.typesafe.play" %% "play-json" % "2.9.2"
libraryDependencies += "redis.clients" % "jedis" % "3.7.0"
libraryDependencies += "org.scalatest" %% "scalatest" % "3.0.8" % Test

//enablePlugins(ProtobufPlugin)

Compile / PB.targets := Seq(
  scalapb.gen() -> (Compile / sourceManaged).value / "scalapb"
)

assemblyMergeStrategy in assembly := {
  case PathList("META-INF", xs @ _*) => MergeStrategy.discard
  case x => MergeStrategy.first
}
