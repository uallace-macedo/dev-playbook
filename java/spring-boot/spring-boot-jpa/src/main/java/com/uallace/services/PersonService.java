package com.uallace.services;

import com.uallace.exception.custom.ResourceNotFoundException;
import com.uallace.model.Person;
import com.uallace.model.enums.Gender;
import com.uallace.repository.PersonRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicLong;
import java.util.logging.Logger;

@Service
public class PersonService {
    private final AtomicLong counter = new AtomicLong();
    private final Logger logger = Logger.getLogger(PersonService.class.getName());

    @Autowired
    PersonRepository repository;

    public List<Person> findAll() {
        logger.info("finding people");
        return repository.findAll();
    }

    public Person findById(Long id) {
        logger.info("finding a person");
        return repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("resource with id " + id + " not found"));
    }

    public Person create(Person person) {
        logger.info("creating person");
        return repository.save(person);
    }

    public Person update(Person person) {
        logger.info("updating user");
        Person old = repository.findById(person.getId())
                .orElseThrow(() -> new ResourceNotFoundException("resource with id " + person.getId() + " not found"));

        if (old.getFirstName() != null) person.setFirstName(old.getFirstName());
        if (old.getLastName() != null) person.setLastName(old.getLastName());
        if (old.getAddress() != null) person.setAddress(old.getAddress());
        if (old.getGender() != null) person.setGender(old.getGender());

        return repository.save(person);
    }

    public Person delete(Person person) {
        logger.info("deleting user");
        Person old = repository.findById(person.getId())
                .orElseThrow(() -> new ResourceNotFoundException("resource with id " + person.getId() + " not found"));

        repository.delete(old);
        return person;
    }
}
