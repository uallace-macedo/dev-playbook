package com.uallace;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class SpringBasicApplication {
	public static void main(String[] args) {
		SpringApplication.run(SpringBasicApplication.class, args);
		System.out.println("Hello, World!");
	}
}
