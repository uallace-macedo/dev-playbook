package com.uallace.services;

import com.uallace.exception.custom.ResourceNotFoundException;
import com.uallace.model.Person;
import com.uallace.repository.PersonRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

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

    public Person update(long id, Person newData) {
        logger.info("updating user");
        Person person = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("resource with id " + id + " not found"));

        if (newData.getFirstName() != null) person.setFirstName(newData.getFirstName());
        if (newData.getLastName() != null) person.setLastName(newData.getLastName());
        if (newData.getAddress() != null) person.setAddress(newData.getAddress());
        if (newData.getGender() != null) person.setGender(newData.getGender());

        return repository.save(person);
    }

    public void delete(long id) {
        logger.info("deleting user");
        Person person = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("resource with id " + id + " not found"));

        repository.delete(person);
    }
}
