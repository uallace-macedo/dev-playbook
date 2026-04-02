package com.uallace.serializer;

import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.databind.JsonSerializer;
import com.fasterxml.jackson.databind.SerializerProvider;
import com.uallace.model.enums.Gender;

import java.io.IOException;

public class GenderSerializer extends JsonSerializer<Gender> {
    @Override
    public void serialize(Gender gender, JsonGenerator gen, SerializerProvider serializerProvider) throws IOException {
        String formatedGen = Gender.MALE == gender ? "M" : "F";
        gen.writeString(formatedGen);
    }
}
