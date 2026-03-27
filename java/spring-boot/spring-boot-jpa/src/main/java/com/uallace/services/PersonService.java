package com.uallace.services;

import com.uallace.dto.PersonDTO;
import com.uallace.exception.custom.ResourceNotFoundException;
import com.uallace.mapper.ObjectMapper;
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

    public List<PersonDTO> findAll() {
        logger.info("finding people");
        return ObjectMapper.parseListObjects(repository.findAll(), PersonDTO.class);
    }

    public PersonDTO findById(Long id) {
        logger.info("finding a person");
        return ObjectMapper.parseObject(
                repository.findById(id).orElseThrow(() -> new ResourceNotFoundException("resource with id " + id + " not found")),
                        PersonDTO.class);

    }

    public PersonDTO create(PersonDTO person) {
        logger.info("creating person");
        Person saved = repository.save(ObjectMapper.parseObject(person, Person.class));
        return ObjectMapper.parseObject(saved, PersonDTO.class);
    }

    public PersonDTO update(long id, PersonDTO newData) {
        logger.info("updating user");
        Person person = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("resource with id " + id + " not found"));

        if (newData.getFirstName() != null) person.setFirstName(newData.getFirstName());
        if (newData.getLastName() != null) person.setLastName(newData.getLastName());
        if (newData.getAddress() != null) person.setAddress(newData.getAddress());
        if (newData.getGender() != null) person.setGender(newData.getGender());

        return ObjectMapper.parseObject(repository.save(person), PersonDTO.class);
    }

    public void delete(long id) {
        logger.info("deleting user");
        Person person = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("resource with id " + id + " not found"));

        repository.delete(person);
    }
}
