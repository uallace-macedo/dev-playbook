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
            @PathVariable("x") double x,
            @PathVariable("y") double y
    ) {
        return x-y;
    }

    // div/x/y
    @RequestMapping("/div/{x}/{y}")
    public double div(
            @PathVariable("x") double x,
            @PathVariable("y") double y
    ) {
        return x/y;
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
