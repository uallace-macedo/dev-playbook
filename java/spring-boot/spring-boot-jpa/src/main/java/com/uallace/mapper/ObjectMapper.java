package com.uallace.mapper;

import com.github.dozermapper.core.DozerBeanMapperBuilder;
import com.github.dozermapper.core.Mapper;

import java.util.ArrayList;
import java.util.List;

public class ObjectMapper {
    private static final Mapper mapper = DozerBeanMapperBuilder.buildDefault();

    public static <O, D> D parseObject(O origin, Class<D> destiny) {
        return mapper.map(origin, destiny);
    }

    public static <O, D> List<D> parseListObjects(List<O> origin, Class<D> destiny) {
        List<D> list = new ArrayList<>();
        origin.forEach(o -> list.add(mapper.map(o, destiny)));
        return list;
    }
}
