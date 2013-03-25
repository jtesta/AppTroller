'''
RandomInfoGenerator.py
Copyright (C) 2013, Joe Testa <jtesta@positronsecurity.com>

This class generates random data to troll with.
'''

import random, os, string, struct
class RandomInfoGenerator:


    # Generates a random telephone number.  Argument may be a partial number,
    # which will be expanded into an entire number. (i.e.: it can have
    # '1212', which this function will then generate the rest of the numbers,
    # yielding a random number in the 212 area code).
    @staticmethod
    def getLineNumber(line_number):

        # Pad the line_number until we have at least 11 digits.  We're too good
        # to use the standard rand() function.... because hey... what if
        # someone uses our phone number as cryptographic key material?  :P
        while len(line_number) < 11:
            bytes = os.urandom(8)
            line_number = line_number + str(struct.unpack('BBBBBBBB', bytes)[0])

        # If the number is too big, trim it so its exactly 11 digits.
        if len(line_number) > 11:
            line_number = line_number[:11]

        return line_number


    # Return a random phone device ID.
    @staticmethod
    def getDeviceID():
        device_id = ''
        while len(device_id) < 15:
            bytes = os.urandom(8)
            device_id = device_id + str(struct.unpack('BBBBBBBB', bytes)[0])

        if len(device_id) > 15:
            device_id = device_id[:15]

        return device_id


    # Return a random SIM serial number.
    @staticmethod
    def getSIMSerialNumber():
        sim_serial_number = ''
        while len(sim_serial_number) < 20:
            bytes = os.urandom(8)
            sim_serial_number = sim_serial_number + str(struct.unpack('BBBBBBBB', bytes)[0])

        if len(sim_serial_number) > 20:
            sim_serial_number = sim_serial_number[:20]

        return sim_serial_number


    # Return a random subscriber ID.
    @staticmethod
    def getSubscriberID():
        subscriber_id = ''
        while len(subscriber_id) < 16:
            bytes = os.urandom(8)
            subscriber_id = subscriber_id + str(struct.unpack('BBBBBBBB', bytes)[0])

        if len(subscriber_id) > 16:
            subscriber_id = subscriber_id[:16]

        return subscriber_id


    # Return a random Google account name.
    @staticmethod
    def getGoogleAccount():
        letters = ''.join(random.choice(string.ascii_lowercase) for x in range(8))
        numbers = ''.join(random.choice(string.digits) for x in range(3))
        return '%s%s@gmail.com' % (letters, numbers)


    # Returns a random tuple containing a random US city and state.
    @staticmethod
    def getCityState():
        cityStates = (('Rochester', 'NY'),('Buffalo', 'NY'),('New York', 'NY'),('Los Angeles', 'CA'),('Washington', 'DC'),('Portland', 'OR'),('Sacramento', 'CA'),('Houston', 'TX'),('Dallas', 'TX'),('Austin', 'TX'),('Philadelphia', 'PA'),('Orlando', 'FL'),('Atlanta', 'GA'),('Minneapolis', 'MN'),('Raleigh', 'NC'),('Las Vegas', 'NV'),('Boston', 'MA'),('Albuquerque', 'NM'),('Phoenix', 'AZ'),('Salt Lake City', 'UT'),('Seatle', 'WA'),('Ann Arbor', 'MI'),('Detroit', 'MI'),('Chicago', 'IL'),('Columbus', 'OH'),('Denver', 'CO'))
        return random.SystemRandom().choice(cityStates)


    # Returns a random first and last name, belonging to a male or female.
    @staticmethod
    def getFirstLastName():
        return '%s %s' % (RandomInfoGenerator.getFirstName(),
                          RandomInfoGenerator.getLastName())


    # Returns a random first name (both male and female).
    @staticmethod
    def getFirstName():
        firstNames = ('James','John','Robert','Michael','William','David','Richard','Charles','Joseph','Thomas','Christopher','Daniel','Paul','Mark','Donald','George','Kenneth','Steven','Edward','Brian','Ronald','Anthony','Kevin','Jason','Matthew','Gary','Timothy','Jose','Larry','Jeffrey','Frank','Scott','Eric','Stephen','Andrew','Raymond','Gregory','Joshua','Jerry','Dennis','Walter','Patrick','Peter','Harold','Douglas','Henry','Carl','Arthur','Ryan','Roger','Joe','Juan','Jack','Albert','Jonathan','Justin','Terry','Gerald','Keith','Samuel','Willie','Ralph','Lawrence','Nicholas','Roy','Benjamin','Bruce','Brandon','Adam','Harry','Fred','Wayne','Billy','Steve','Louis','Jeremy','Aaron','Randy','Howard','Eugene','Carlos','Russell','Bobby','Victor','Martin','Ernest','Phillip','Todd','Jesse','Craig','Alan','Shawn','Clarence','Sean','Philip','Chris','Johnny','Earl','Jimmy','Antonio','Danny','Bryan','Tony','Luis','Mike','Stanley','Leonard','Nathan','Dale','Manuel','Rodney','Curtis','Norman','Allen','Marvin','Vincent','Glenn','Jeffery','Travis','Jeff','Chad','Jacob','Lee','Melvin','Alfred','Kyle','Francis','Bradley','Jesus','Herbert','Frederick','Ray','Joel','Edwin','Don','Eddie','Ricky','Troy','Randall','Barry','Alexander','Bernard','Mario','Leroy','Francisco','Marcus','Micheal','Theodore','Clifford','Miguel','Oscar','Jay','Jim','Tom','Calvin','Alex','Jon','Ronnie','Bill','Lloyd','Tommy','Leon','Derek','Warren','Darrell','Jerome','Floyd','Leo','Alvin','Tim','Wesley','Gordon','Dean','Greg','Jorge','Dustin','Pedro','Derrick','Dan','Lewis','Zachary','Corey','Herman','Maurice','Vernon','Roberto','Clyde','Glen','Hector','Shane','Ricardo','Sam','Rick','Lester','Brent','Ramon','Charlie','Tyler','Gilbert','Gene','Marc','Reginald','Ruben','Brett','Angel','Nathaniel','Rafael','Leslie','Edgar','Milton','Raul','Ben','Chester','Cecil','Duane','Franklin','Andre','Elmer','Brad','Gabriel','Ron','Mitchell','Roland','Arnold','Harvey','Jared','Adrian','Karl','Cory','Claude','Erik','Darryl','Jamie','Neil','Jessie','Christian','Javier','Fernando','Clinton','Ted','Mathew','Tyrone','Darren','Lonnie','Lance','Cody','Julio','Kelly','Kurt','Allan','Nelson','Guy','Clayton','Hugh','Max','Dwayne','Dwight','Armando','Felix','Jimmie','Everett','Jordan','Ian','Wallace','Ken','Bob','Jaime','Casey','Alfredo','Alberto','Dave','Ivan','Johnnie','Sidney','Byron','Julian','Isaac','Morris','Clifton','Willard','Daryl','Ross','Virgil','Andy','Marshall','Salvador','Perry','Kirk','Sergio','Marion','Tracy','Seth','Kent','Terrance','Rene','Eduardo','Terrence','Enrique','Freddie','Wade','Mary','Patricia','Linda','Barbara','Elizabeth','Jennifer','Maria','Susan','Margaret','Dorothy','Lisa','Nancy','Karen','Betty','Helen','Sandra','Donna','Carol','Ruth','Sharon','Michelle','Laura','Sarah','Kimberly','Deborah','Jessica','Shirley','Cynthia','Angela','Melissa','Brenda','Amy','Anna','Rebecca','Virginia','Kathleen','Pamela','Martha','Debra','Amanda','Stephanie','Carolyn','Christine','Marie','Janet','Catherine','Frances','Ann','Joyce','Diane','Alice','Julie','Heather','Teresa','Doris','Gloria','Evelyn','Jean','Cheryl','Mildred','Katherine','Joan','Ashley','Judith','Rose','Janice','Kelly','Nicole','Judy','Christina','Kathy','Theresa','Beverly','Denise','Tammy','Irene','Jane','Lori','Rachel','Marilyn','Andrea','Kathryn','Louise','Sara','Anne','Jacqueline','Wanda','Bonnie','Julia','Ruby','Lois','Tina','Phyllis','Norma','Paula','Diana','Annie','Lillian','Emily','Robin','Peggy','Crystal','Gladys','Rita','Dawn','Connie','Florence','Tracy','Edna','Tiffany','Carmen','Rosa','Cindy','Grace','Wendy','Victoria','Edith','Kim','Sherry','Sylvia','Josephine','Thelma','Shannon','Sheila','Ethel','Ellen','Elaine','Marjorie','Carrie','Charlotte','Monica','Esther','Pauline','Emma','Juanita','Anita','Rhonda','Hazel','Amber','Eva','Debbie','April','Leslie','Clara','Lucille','Jamie','Joanne','Eleanor','Valerie','Danielle','Megan','Alicia','Suzanne','Michele','Gail','Bertha','Darlene','Veronica','Jill','Erin','Geraldine','Lauren','Cathy','Joann','Lorraine','Lynn','Sally','Regina','Erica','Beatrice','Dolores','Bernice','Audrey','Yvonne','Annette','June','Samantha','Marion','Dana','Stacy','Ana','Renee','Ida','Vivian','Roberta','Holly','Brittany','Melanie','Loretta','Yolanda','Jeanette','Laurie','Katie','Kristen','Vanessa','Alma','Sue','Elsie','Beth','Jeanne','Vicki','Carla','Tara','Rosemary','Eileen','Terri','Gertrude','Lucy','Tonya','Ella','Stacey','Wilma','Gina','Kristin','Jessie','Natalie','Agnes','Vera','Willie','Charlene','Bessie','Delores','Melinda','Pearl','Arlene','Maureen','Colleen','Allison','Tamara','Joy','Georgia','Constance','Lillie','Claudia','Jackie','Marcia','Tanya','Nellie','Minnie','Marlene','Heidi','Glenda','Lydia','Viola','Courtney','Marian','Stella','Caroline','Dora','Jo','Vickie','Mattie','Terry','Maxine','Irma','Mabel','Marsha','Myrtle','Lena','Christy','Deanna','Patsy','Hilda','Gwendolyn','Jennie','Nora','Margie','Nina','Cassandra','Leah','Penny','Kay','Priscilla','Naomi','Carole','Brandy','Olga','Billie','Dianne','Tracey','Leona','Jenny','Felicia','Sonia','Miriam','Velma','Becky','Bobbie','Violet','Kristina','Toni','Misty','Mae','Shelly','Daisy','Ramona','Sherri','Erika','Katrina','Claire')
        return random.SystemRandom().choice(firstNames)


    # Returns a random last name.
    @staticmethod
    def getLastName():
        lastNames = ('Smith','Johnson','Williams','Jones','Brown','Davis','Miller','Wilson','Moore','Taylor','Anderson','Thomas','Jackson','White','Harris','Martin','Thompson','Garcia','Martinez','Robinson','Clark','Rodriguez','Lewis','Lee','Walker','Hall','Allen','Young','Hernandez','King','Wright','Lopez','Hill','Scott','Green','Adams','Baker','Gonzalez','Nelson','Carter','Mitchell','Perez','Roberts','Turner','Phillips','Campbell','Parker','Evans','Edwards','Collins','Stewart','Sanchez','Morris','Rogers','Reed','Cook','Morgan','Bell','Murphy','Bailey','Rivera','Cooper','Richardson','Cox','Howard','Ward','Torres','Peterson','Gray','Ramirez','James','Watson','Brooks','Kelly','Sanders','Price','Bennett','Wood','Barnes','Ross','Henderson','Coleman','Jenkins','Perry','Powell','Long','Patterson','Hughes','Flores','Washington','Butler','Simmons','Foster','Gonzales','Bryant','Alexander','Russell','Griffin','Diaz','Hayes','Myers','Ford','Hamilton','Graham','Sullivan','Wallace','Woods','Cole','West','Jordan','Owens','Reynolds','Fisher','Ellis','Harrison','Gibson','Mcdonald','Cruz','Marshall','Ortiz','Gomez','Murray','Freeman','Wells','Webb','Simpson','Stevens','Tucker','Porter','Hunter','Hicks','Crawford','Henry','Boyd','Mason','Morales','Kennedy','Warren','Dixon','Ramos','Reyes','Burns','Gordon','Shaw','Holmes','Rice','Robertson','Hunt','Black','Daniels','Palmer','Mills','Nichols','Grant','Knight','Ferguson','Rose','Stone','Hawkins','Dunn','Perkins','Hudson','Spencer','Gardner','Stephens','Payne','Pierce','Berry','Matthews','Arnold','Wagner','Willis','Ray','Watkins','Olson','Carroll','Duncan','Snyder','Hart','Cunningham','Bradley','Lane','Andrews','Ruiz','Harper','Fox','Riley','Armstrong','Carpenter','Weaver','Greene','Lawrence','Elliott','Chavez','Sims','Austin','Peters','Kelley','Franklin','Lawson','Fields','Gutierrez','Ryan','Schmidt','Carr','Vasquez','Castillo','Wheeler','Chapman','Oliver','Montgomery','Richards','Williamson','Johnston','Banks','Meyer','Bishop','Mccoy','Howell','Alvarez','Morrison','Hansen','Fernandez','Garza','Harvey','Little','Burton','Stanley','Nguyen','George','Jacobs','Reid','Kim','Fuller','Lynch','Dean','Gilbert','Garrett','Romero','Welch','Larson','Frazier','Burke','Hanson','Day','Mendoza','Moreno','Bowman','Medina','Fowler','Brewer','Hoffman','Carlson','Silva','Pearson','Holland','Douglas','Fleming','Jensen','Vargas','Byrd','Davidson','Hopkins','May','Terry','Herrera','Wade','Soto','Walters','Curtis','Neal','Caldwell','Lowe','Jennings','Barnett','Graves','Jimenez','Horton','Shelton','Barrett','Obrien','Castro','Sutton','Gregory','Mckinney','Lucas','Miles','Craig','Rodriquez','Chambers','Holt','Lambert','Fletcher','Watts','Bates','Hale','Rhodes','Pena','Beck','Newman','Haynes','Mcdaniel','Mendez','Bush','Vaughn','Parks','Dawson','Santiago','Norris','Hardy','Love','Steele','Curry','Powers','Schultz','Barker','Guzman','Page','Munoz','Ball','Keller','Chandler','Weber','Leonard','Walsh','Lyons','Ramsey','Wolfe','Schneider','Mullins','Benson','Sharp','Bowen','Daniel','Barber','Cummings','Hines','Baldwin','Griffith','Valdez','Hubbard','Salazar','Reeves','Warner','Stevenson','Burgess','Santos','Tate','Cross','Garner','Mann','Mack','Moss','Thornton','Dennis','Mcgee','Farmer','Delgado','Aguilar','Vega','Glover','Manning','Cohen','Harmon','Rodgers','Robbins','Newton','Todd','Blair','Higgins','Ingram','Reese','Cannon','Strickland','Townsend','Potter','Goodwin','Walton','Rowe','Hampton','Ortega','Patton','Swanson','Joseph','Francis','Goodman','Maldonado','Yates','Becker','Erickson','Hodges','Rios','Conner','Adkins','Webster','Norman','Malone','Hammond','Flowers','Cobb','Moody','Quinn','Blake','Maxwell','Pope','Floyd','Osborne','Paul','Mccarthy','Guerrero','Lindsey','Estrada','Sandoval','Gibbs','Tyler','Gross','Fitzgerald','Stokes','Doyle','Sherman','Saunders','Wise','Colon','Gill','Alvarado','Greer','Padilla','Simon','Waters','Nunez','Ballard','Schwartz','Mcbride','Houston','Christensen','Klein','Pratt','Briggs','Parsons','Mclaughlin','Zimmerman','French','Buchanan','Moran','Copeland','Roy','Pittman','Brady','Mccormick','Holloway','Brock','Poole','Frank','Logan','Owen','Bass','Marsh','Drake','Wong','Jefferson','Park','Morton','Abbott','Sparks','Patrick','Norton','Huff','Clayton','Massey','Lloyd','Figueroa','Carson','Bowers','Roberson','Barton','Tran','Lamb','Harrington','Casey','Boone','Cortez','Clarke','Mathis','Singleton','Wilkins','Cain','Bryan','Underwood','Hogan','Mckenzie','Collier','Luna','Phelps','Mcguire','Allison','Bridges','Wilkerson','Nash','Summers','Atkins','Wilcox','Pitts','Conley','Marquez','Burnett','Richard','Cochran','Chase','Davenport','Hood','Gates','Clay','Ayala','Sawyer','Roman','Vazquez','Dickerson','Hodge','Acosta','Flynn','Espinoza','Nicholson','Monroe','Wolf','Morrow','Kirk','Randall','Anthony','Whitaker','Oconnor','Skinner','Ware','Molina','Kirby','Huffman','Bradford','Charles','Gilmore','Dominguez','Oneal','Bruce','Lang','Combs','Kramer','Heath','Hancock','Gallagher','Gaines','Shaffer','Short','Wiggins','Mathews','Mcclain','Fischer','Wall','Small','Melton','Hensley','Bond','Dyer','Cameron','Grimes','Contreras','Christian','Wyatt','Baxter','Snow','Mosley','Shepherd','Larsen','Hoover','Beasley','Glenn','Petersen','Whitehead','Meyers','Keith','Garrison','Vincent','Shields','Horn','Savage','Olsen','Schroeder','Hartman','Woodard','Mueller','Kemp','Deleon','Booth','Patel','Calhoun','Wiley','Eaton','Cline','Navarro','Harrell','Lester','Humphrey','Parrish','Duran','Hutchinson','Hess','Dorsey','Bullock','Robles','Beard','Dalton','Avila','Vance','Rich','Blackwell','York','Johns','Blankenship','Trevino','Salinas','Campos','Pruitt','Moses','Callahan','Golden','Montoya','Hardin','Guerra','Mcdowell','Carey','Stafford','Gallegos','Henson','Wilkinson','Booker','Merritt','Miranda','Atkinson','Orr','Decker','Hobbs','Preston','Tanner','Knox','Pacheco','Stephenson','Glass','Rojas','Serrano','Marks','Hickman','English','Sweeney','Strong','Prince','Mcclure','Conway','Walter','Roth','Maynard','Farrell','Lowery','Hurst','Nixon','Weiss','Trujillo','Ellison','Sloan','Juarez','Winters','Mclean','Randolph','Leon','Boyer','Villarreal','Mccall','Gentry','Carrillo','Kent','Ayers','Lara','Shannon','Sexton','Pace','Hull','Leblanc','Browning','Velasquez','Leach','Chang','House','Sellers','Herring','Noble','Foley','Bartlett','Mercado','Landry','Durham','Walls','Barr','Mckee','Bauer','Rivers','Everett','Bradshaw','Pugh','Velez','Rush','Estes','Dodson','Morse','Sheppard','Weeks','Camacho','Bean','Barron','Livingston','Middleton','Spears','Branch','Blevins','Chen','Kerr','Mcconnell','Hatfield','Harding','Ashley','Solis','Herman','Frost','Giles','Blackburn','William','Pennington','Woodward','Finley','Mcintosh','Koch','Best','Solomon','Mccullough','Dudley','Nolan','Blanchard','Rivas','Brennan','Mejia','Kane','Benton','Joyce','Buckley','Haley','Valentine','Maddox','Russo','Mcknight','Buck','Moon','Mcmillan','Crosby','Berg','Dotson','Mays','Roach','Church','Chan','Richmond','Meadows','Faulkner','Oneill','Knapp','Kline','Barry','Ochoa','Jacobson','Gay','Avery','Hendricks','Horne','Shepard','Hebert','Cherry','Cardenas','Mcintyre','Whitney','Waller','Holman','Donaldson','Cantu','Terrell','Morin','Gillespie','Fuentes','Tillman','Sanford','Bentley','Peck','Key','Salas','Rollins','Gamble','Dickson','Battle','Santana','Cabrera','Cervantes','Howe','Hinton','Hurley','Spence','Zamora','Yang','Mcneil','Suarez','Case','Petty','Gould','Mcfarland','Sampson','Carver','Bray','Rosario','Macdonald','Stout','Hester','Melendez','Dillon','Farley','Hopper','Galloway','Potts','Bernard','Joyner','Stein','Aguirre','Osborn','Mercer','Bender','Franco','Rowland','Sykes','Benjamin','Travis','Pickett','Crane','Sears','Mayo','Dunlap','Hayden','Wilder','Mckay','Coffey','Mccarty','Ewing','Cooley','Vaughan','Bonner','Cotton','Holder','Stark','Ferrell','Cantrell','Fulton','Lynn','Lott','Calderon','Rosa','Pollard','Hooper','Burch','Mullen','Fry','Riddle','Levy','David','Duke','Odonnell','Guy','Michael','Britt','Frederick','Daugherty','Berger','Dillard','Alston','Jarvis','Frye','Riggs','Chaney','Odom','Duffy','Fitzpatrick','Valenzuela','Merrill','Mayer','Alford','Mcpherson','Acevedo','Donovan','Barrera','Albert','Cote','Reilly','Compton','Raymond','Mooney','Mcgowan','Craft','Cleveland','Clemons','Wynn','Nielsen','Baird','Stanton','Snider','Rosales','Bright','Witt','Stuart','Hays','Holden','Rutledge','Kinney','Clements','Castaneda','Slater','Hahn','Emerson','Conrad','Burks','Delaney','Pate','Lancaster','Sweet','Justice','Tyson','Sharpe','Whitfield','Talley','Macias','Irwin','Burris','Ratliff','Mccray','Madden','Kaufman','Beach','Goff','Cash','Bolton','Mcfadden','Levine','Good','Byers','Kirkland','Kidd','Workman','Carney','Dale','Mcleod','Holcomb','England','Finch','Head','Burt','Hendrix','Sosa','Haney','Franks','Sargent','Nieves','Downs','Rasmussen','Bird','Hewitt','Lindsay','Le','Foreman','Valencia','Oneil','Delacruz','Vinson','Dejesus','Hyde','Forbes','Gilliam','Guthrie','Wooten','Huber','Barlow','Boyle','Mcmahon','Buckner','Rocha','Puckett','Langley','Knowles','Cooke','Velazquez','Whitley','Noel','Vang')
        return random.SystemRandom().choice(lastNames)
