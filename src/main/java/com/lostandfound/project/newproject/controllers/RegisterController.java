package com.lostandfound.project.newproject.controllers;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;


@RestController
public class RegisterController {
    @PostMapping("/register")
    public String Register(@RequestBody String entity) {
        //TODO: process POST request
        
        return entity;
    }
    
    
}
