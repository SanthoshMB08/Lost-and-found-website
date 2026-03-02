package com.dev.LAF.controllers;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/laf/v1/auth")
public class AuthController {

    @PostMapping("/register")
    public String register() {
        return "User registered successfully!";
    }
    @PostMapping("/login")
    public String login() {
        return "User logged in successfully!";
    }
    @PutMapping("/reset-password")
    public String resetPassword() {
        return "Password reset successfully!";
    }
    @GetMapping("/find-user")
    public String findUser() {
        return "User found successfully!";
    }
}
