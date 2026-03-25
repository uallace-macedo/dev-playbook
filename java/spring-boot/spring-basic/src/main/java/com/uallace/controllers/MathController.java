package com.uallace.controllers;

import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/math")
public class MathController {
    // sum/x/y
    @RequestMapping("/sum/{x}/{y}")
    public double sum(
            @PathVariable("x") String x,
            @PathVariable("y") String y
    ) {
        if (isNumeric(x) || isNumeric(y)) throw new IllegalArgumentException("please provide valid numbers");
        return convertToDouble(x) + convertToDouble(y);
    }

    // sub/x/y
    @RequestMapping("/sub/{x}/{y}")
    public double sub(
            @PathVariable("x") String x,
            @PathVariable("y") String y
    ) {
        if (isNumeric(x) || isNumeric(y)) throw new IllegalArgumentException("please provide valid numbers");
        return convertToDouble(x) - convertToDouble(y);
    }

    // div/x/y
    @RequestMapping("/div/{x}/{y}")
    public double div(
            @PathVariable("x") String x,
            @PathVariable("y") String y
    ) {
        if (isNumeric(x) || isNumeric(y)) throw new IllegalArgumentException("please provide valid numbers");
        return convertToDouble(x) / convertToDouble(y);
    }

    // mult/x/y
    @RequestMapping("/times/{x}/{y}")
    public double times(
            @PathVariable("x") String x,
            @PathVariable("y") String y
    ) {
        if (isNumeric(x) || isNumeric(y)) throw new IllegalArgumentException("please provide valid numbers");
        return convertToDouble(x) * convertToDouble(y);
    }

    // times/x/y
    @RequestMapping("/avg/{x}/{y}")
    public double avg(
            @PathVariable("x") String x,
            @PathVariable("y") String y
    ) {
        if (isNumeric(x) || isNumeric(y)) throw new IllegalArgumentException("please provide valid numbers");
        return (convertToDouble(x) + convertToDouble(y)) / 2;
    }

    // times/x/y
    @RequestMapping("/sqrt/{x}")
    public double sqrt(
            @PathVariable("x") String x
    ) {
        if (isNumeric(x)) throw new IllegalArgumentException("please provide valid numbers");
        return Math.sqrt(convertToDouble(x));
    }

    private boolean isNumeric(String n) {
        if (n == null || n.isEmpty())  return true;
        String number = n.replace(",", ".");
        return !number.matches("[-+]?[0-9]*\\.?[0-9]+");
    }

    private double convertToDouble(String n) {
        return Double.parseDouble(n);
    }
}
