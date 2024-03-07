FROM flink:1.18
ADD target/flink-autoscaler-standalone-1.8-SNAPSHOT.jar app.jar
ENTRYPOINT ["java", "-cp", "app.jar", "org.apache.flink.autoscaler.standalone.StandaloneAutoscalerEntrypoint", "--flinkClusterHost", "localhost", "--flinkClusterPort", "8081"]
