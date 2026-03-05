package com.dev.LAF.controllers;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.PathVariable;




@RestController
@RequestMapping("/api/laf/v1/profile")
public class ProfileController {
    @GetMapping("/user-post")
    public String userPost (@RequestParam String param) {
        return new String();
    }
    
    @GetMapping("/user-data")
    public String getUserData(@RequestParam String param) {
        return new String();
    }

    @GetMapping("/get-followers")
    public String getFollowers(@RequestParam String param) {
        return new String();
    }
   @GetMapping("/get-following")
    public String getFollowing(@RequestParam String param) {
        return new String();
    }
    @PutMapping("/update-profile")
    public String updateProfile(@RequestParam String param) {
        return new String();
    }
    @PutMapping("/update-following")
    public String updateFollowing( @RequestBody String entity) {
        
        return entity;
    }
    @PutMapping("/update-follower")
    public String updateFollower( @RequestBody String entity) {
        
        return entity;
    }
    
    
}
