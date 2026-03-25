package com.uallace.services;

import com.uallace.model.Person;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicLong;
import java.util.logging.Logger;

@Service
public class PersonService {
    private final AtomicLong counter = new AtomicLong();
    private final Logger logger = Logger.getLogger(PersonService.class.getName());

    public List<Person> findAll() {
        logger.info("finding people");
        List<Person> people = new ArrayList<Person>();

        for(int i = 0; i < 8; i++) {
            Person person = mockPerson(i);
            people.add(person);
        }

        return people;
    }

    public Person findById(String id) {
        logger.info("finding a person");
        Person person = new Person();

        person.setId(counter.incrementAndGet());
        person.setFirstName("John");
        person.setLastName("Santos");
        person.setAddress("Salvador - BA");
        person.setGender("Male");

        return person;
    }

    public Person create(Person person) {
        person.setId(counter.incrementAndGet());
        return person;
    }

    private Person mockPerson(int i) {
        Person person = new Person();
        person.setId(counter.incrementAndGet());
        person.setFirstName("Mock Person " + i);
        person.setLastName("Mock Last Name " + i);
        person.setAddress("Mock Address " + i);
        person.setGender(i % 2 == 0 ? "Female" : "Male");
        return person;
    }
}
