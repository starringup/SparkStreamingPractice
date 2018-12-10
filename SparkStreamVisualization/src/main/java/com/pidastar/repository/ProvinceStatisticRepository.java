package com.pidastar.repository;

import org.springframework.data.mongodb.repository.MongoRepository;

import com.pidastar.entity.ProvinceStatistic;

public interface ProvinceStatisticRepository extends MongoRepository<ProvinceStatistic, String>
{
	
}
