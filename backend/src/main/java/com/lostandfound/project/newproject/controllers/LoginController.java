package com.lostandfound.project.newproject.controllers;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;


@RestController

public class LoginController {
    @GetMapping("/login")
    public String getMethodName(@RequestParam String Username , @RequestParam String Password) {
        return "Login successful for user: " + Username;
    }
    
    
}
