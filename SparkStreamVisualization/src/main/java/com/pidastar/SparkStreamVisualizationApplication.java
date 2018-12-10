package com.pidastar;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;

@SpringBootApplication(exclude={DataSourceAutoConfiguration.class})
public class SparkStreamVisualizationApplication {

	public static void main(String[] args) {
		SpringApplication.run(SparkStreamVisualizationApplication.class, args);
	}
}
