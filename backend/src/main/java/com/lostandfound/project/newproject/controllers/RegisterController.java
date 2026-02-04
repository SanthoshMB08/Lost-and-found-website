package com.lostandfound.project.newproject.controllers;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;


@RestController
public class RegisterController {
    @PostMapping("/register")
    public String Register(@RequestParam String username) {
       
        
        return "hello " + username;
    }
    
    
}
