-- MySQL Script generated by MySQL Workbench
-- Mon Feb 27 19:46:24 2023
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema socfilms_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema socfilms_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `socfilms_db` DEFAULT CHARACTER SET utf8 ;
USE `socfilms_db` ;

-- -----------------------------------------------------
-- Table `socfilms_db`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `socfilms_db`.`users` (
  `idusers` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `surname` VARCHAR(45) NOT NULL,
  `nickname` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `country` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idusers`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `socfilms_db`.`films`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `socfilms_db`.`films` (
  `idfilms` INT NOT NULL AUTO_INCREMENT,
  `filmname` VARCHAR(45) NOT NULL,
  `year` YEAR NOT NULL,
  `genre` VARCHAR(45) NOT NULL,
  `country` VARCHAR(45) NULL,
  PRIMARY KEY (`idfilms`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `socfilms_db`.`favouritefilms`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `socfilms_db`.`favouritefilms` (
  `idfavouritefilms` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `film_id` INT NOT NULL,
  `add_date` DATE NOT NULL,
  `rating` TINYINT(2) NOT NULL,
  `comments` VARCHAR(200) NULL,
  PRIMARY KEY (`idfavouritefilms`),
  INDEX `users_idx` (`user_id` ASC) VISIBLE,
  INDEX `films_idx` (`film_id` ASC) VISIBLE,
  CONSTRAINT `users`
    FOREIGN KEY (`user_id`)
    REFERENCES `socfilms_db`.`users` (`idusers`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `films`
    FOREIGN KEY (`film_id`)
    REFERENCES `socfilms_db`.`films` (`idfilms`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `socfilms_db`.`friends`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `socfilms_db`.`friends` (
  `idfriends` INT NOT NULL AUTO_INCREMENT,
  `main_user` INT NOT NULL,
  `friend_user` INT NOT NULL,
  `status` VARCHAR(20) NOT NULL DEFAULT 'asked',
  PRIMARY KEY (`idfriends`),
  INDEX `main_idx` (`main_user` ASC) VISIBLE,
  INDEX `friend_idx` (`friend_user` ASC) VISIBLE,
  CONSTRAINT `main`
    FOREIGN KEY (`main_user`)
    REFERENCES `socfilms_db`.`users` (`idusers`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `friend`
    FOREIGN KEY (`friend_user`)
    REFERENCES `socfilms_db`.`users` (`idusers`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
