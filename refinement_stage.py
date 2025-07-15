## VASILEIOS MPINAS
## 4434

##### second part ################

### Create a list from grid.dir
def create_directory_list(directory_reader):

    directory_list=[]

    for row in directory_reader:
        row=row.replace('\n','')
        directory_list.append(row)

    directory_list.remove(directory_list[0])

    for i in range(len(directory_list)):
        directory_list[i]=directory_list[i].split(' ')

        for j in range(len(directory_list[i])):
            directory_list[i][j]=int(directory_list[i][j])
    
    return directory_list


### Create a list from grid.grd
def create_grid_list(grd_reader):
     
    grd_list=[]

    for row in grd_reader:
        row=row.replace('\n','')
        grd_list.append(row)

    grd_list.remove(grd_list[0])

    for i in range(len(grd_list)):
        grd_list[i]=grd_list[i].split('|')
        grd_list[i][2]=grd_list[i][2].split('/')

        grd_list[i][2].remove(grd_list[i][2][-1])

        for j in range(len(grd_list[i][2])):
            grd_list[i][2][j]=grd_list[i][2][j].split(',')
            grd_list[i][2][j][0]=float(grd_list[i][2][j][0])
            grd_list[i][2][j][1]=float(grd_list[i][2][j][1])
    return grd_list


### Creates the grid

def grid_maker(max_X,min_X,max_Y,min_Y):
    x_distance=[]       ### A list with x values on the axis
    y_distance=[]       ### A list with y values on the axis
    grid_ofX=[]         ### A list that contains all the x_distance lists
    grid_ofY=[]         ### ### A list that contains all the y_distance lists
    

    for i in range(0,10):
        x_distance.append(min_X+i*(max_X-min_X)/10)
        x_distance.append(min_X+(i+1)*(max_X-min_X)/10)
        grid_ofX.append(x_distance)
        x_distance=[]

        y_distance.append(min_Y+i*(max_Y-min_Y)/10)
        y_distance.append(min_Y+(i+1)*(max_Y-min_Y)/10)
        grid_ofY.append(y_distance)
        y_distance=[]
    
    return grid_ofX,grid_ofY



### Find the ID of the linestings inside the cells

def find_id(querry,c_list,cell_id,g_list,id_list):
    ids=[]
    final_id_list=[]
    for i in range(0,len(cell_id)):
        #### sum the 4th coloumn of grid.dir until you get to cell_id[i][0]-2 ###
        start_count=c_list[0]
        for j in range(1,cell_id[i][0]-2):
            start_count+=c_list[j]


        start_count-=1
        
        counter=0
        j=0

        while j <cell_id[i][3]:
            ### Check if the reference points are inside the MBR or the window

            ### In the case a point from the MBR is inside the window
            if querry[1]>=g_list[start_count+j][0] and querry[1]<g_list[start_count+j][2] and querry[3]>=g_list[start_count+j][1] and querry[3]<g_list[start_count+j][3]:
                counter+=1

            if querry[2]>=g_list[start_count+j][0] and querry[2]<g_list[start_count+j][2] and querry[3]>=g_list[start_count+j][1] and querry[3]<g_list[start_count+j][3]:
                counter+=1

            if querry[1]>=g_list[start_count+j][0] and querry[1]<g_list[start_count+j][2] and querry[4]>=g_list[start_count+j][1] and querry[4]<g_list[start_count+j][3]:
                counter+=1
            
            if querry[2]>=g_list[start_count+j][0] and querry[2]<g_list[start_count+j][2] and querry[4]>=g_list[start_count+j][1] and querry[4]<g_list[start_count+j][3]:
                counter+=1
            


            ### In the case a point from the window is inside the MBR
            if g_list[start_count+j][0]>=querry[1] and g_list[start_count+j][0]<querry[2] and g_list[start_count+j][1]>=querry[3] and g_list[start_count+j][1]<querry[4]:
                counter+=1

            if g_list[start_count+j][2]>=querry[1] and g_list[start_count+j][2]<querry[2] and g_list[start_count+j][3]>=querry[3] and g_list[start_count+j][3]<querry[4]:
                counter+=1

            if g_list[start_count+j][2]>=querry[1] and g_list[start_count+j][2]<querry[2] and g_list[start_count+j][1]>=querry[3] and g_list[start_count+j][1]<querry[4]:
                counter+=1
            
            if g_list[start_count+j][0]>=querry[1] and g_list[start_count+j][0]<querry[2] and g_list[start_count+j][3]>=querry[3] and g_list[start_count+j][3]<querry[4]:
                counter+=1


            ### When counter>=1 add the ID from id_list to the list ids
            if counter>=1:
                ids.append(id_list[start_count+j])

            counter=0
            j+=1

        ### Add the list ids in final_id_list
        for k in range(len(ids)):
            if ids[k] not in final_id_list:
                final_id_list.append(ids[k])
        ids=[]

    return final_id_list



#### Find the Cells and go check their contents

def find_cell(d_list,c_list,q_list,xlist,ylist,g_list,id_list):
    cells=[]
    seen_cells=[]
    finished_cell_list=[]


    ### FINDING THE CELL  ####
    for i in range(0,len(q_list)):
            x_value_distance=0          ### x_value_distance = x_value2 - x_value1
            y_value_distance=0          ### y_value_distance = y_value2 - y_value1
            x_value1=0
            x_value2=0
            y_value1=0
            y_value2=0


            x_check=0
            y_check=0
            distance_check=0
            j=0
            c2=0

            ### When distance_check == 2 stop the while loop because both x_value_distance and y_value_distance have been calculated
            while distance_check<2:
                # for the distance of x
                if q_list[i][1]>=xlist[j][0] and q_list[i][1]<=xlist[j][1]:
                        x_value1=j
                        x_check+=1

                if q_list[i][2]>=xlist[j][0] and q_list[i][2]<=xlist[j][1]:
                        x_value2=j
                        x_check+=1
                
                # for the distance of y
                if q_list[i][3]>=ylist[j][0] and q_list[i][3]<=ylist[j][1]:
                        y_value1=j
                        y_check+=1
                
                if q_list[i][4]>=ylist[j][0] and q_list[i][4]<=ylist[j][1]:
                        y_value2=j
                        y_check+=1

                ### when x_check or y_check are equal to 2 calculate x_value_distance and y_value_distance
                if x_check==2:
                    x_value_distance=x_value2-x_value1+1
                    x_check=0
                    distance_check+=1
                
                if y_check==2:
                    y_value_distance=y_value2-y_value1+1
                    y_check=0
                    distance_check+=1
                
                j+=1
            distance_check=0
    
            #### Append in the list cells the cells that the window will see
            for x in range (x_value_distance):
                for y in range(y_value_distance):
                    if d_list[(x_value1+x)*10+(y_value1+y)][3]!=0:
                        cells.append(d_list[(x_value1+x)*10+(y_value1+y)])
                    c2+=1                    
               

            seen_cells.append(cells)
            cells=[]



    ####  FINDING THE ID #####
    for i in range(len(q_list)):
        finished_cell_list.append(find_id(q_list[i],c_list,seen_cells[i],g_list,id_list))
    

    return seen_cells,finished_cell_list



###### third part  #######

### Function that makes a list of the MBR and the ID from a given list
def find_MBRandID(g_list):
    ID_list=[]
    MBR_list=[]


    for i in range(len(g_list)):
        ID_list.append(g_list[i][0])
        MBR_list.append(g_list[i][1])
        MBR_list[i]=MBR_list[i].split(',')
        MBR_list[i].remove(MBR_list[i][4])
        for j in range(len(MBR_list[i])):
             MBR_list[i][j]=float(MBR_list[i][j])

    return ID_list,MBR_list


### Function that makes a list based on the ID that are inside the cells (I use it to check the x and y axis and the individual lines)
def create_grid_list_with_ids(id_list,g_list):
    grd_list=[]

    for i in range(0,len(id_list)):
        new_g_list=[]

        for j in range(0,len(g_list)):
            if g_list[j][0] in id_list[i]:
                if g_list[j] not in new_g_list:
                    new_g_list.append(g_list[j])

        grd_list.append(new_g_list)  

    return grd_list


###  Function to check the x and y axis and individual lines and return the ID of the 
def check_axis(q_list,mbr,id_of_list,grd_list):
    id_to_stay=[]

    for i in range(len(mbr)):
            ### For x axis
            if q_list[1]<=mbr[i][0] and q_list[1]<=mbr[i][2] and q_list[2]>=mbr[i][0] and q_list[2]>=mbr[i][2]:
                id_to_stay.append(id_of_list[i])
            
            ### For y axis
            elif q_list[3]<=mbr[i][1] and q_list[3]<=mbr[i][3]and q_list[4]>=mbr[i][1] and q_list[4]>=mbr[i][3]:
                id_to_stay.append(id_of_list[i])
    
            else:
        ### need to check all the values of grd_list
                idr=check_lines(q_list,grd_list)
                id_to_stay.append(idr)
            
    return id_to_stay


def check_lines(q_list,p_list):
    #### x1=q_list[1]   x2=q_list[2]    y1=q_list[3]    y2=q_list[4]
    #### x3=
    id_to_remove=[]

    for j in range(0,len(p_list)):
        for i in range(1,len(p_list[j][2])):
            ### The cases represent the comparisson of the line and the four sides of the window
            ### First case
            if  ((q_list[1]-q_list[1]) * (p_list[j][2][i-1][1]-p_list[j][2][i][1]) - (q_list[3]-q_list[4])*(p_list[j][2][i-1][0]-p_list[j][2][i][0])) != 0:
                t=((q_list[1]-p_list[j][2][i-1][0]) * (p_list[j][2][i-1][1]-p_list[j][2][i][1]) - (q_list[3]-p_list[j][2][i-1][1]) * (p_list[j][2][i-1][0]-p_list[j][2][i][0]))  /  ((q_list[1]-q_list[1]) * (p_list[j][2][i-1][1]-p_list[j][2][i][1]) - (q_list[3]-q_list[4])*(p_list[j][2][i-1][0]-p_list[j][2][i][0]))                                      
                u=((q_list[1]-p_list[j][2][i-1][0]) * (q_list[3]-q_list[4]) - (q_list[3]-p_list[j][2][i-1][1]) * (q_list[1]-q_list[1]))  /  ((q_list[1]-q_list[1]) * (p_list[j][2][i-1][1]-p_list[j][2][i][1]) - (q_list[3]-q_list[4]) * (p_list[j][2][i-1][0]-p_list[j][2][i][0]))                                      
            
            if (t>=0 and t<=1) and (u>=0 and u<=1):
                return p_list[j][0]
            

            ### Second Case
            if  ((q_list[2]-q_list[2]) * (p_list[j][2][i-1][1]-p_list[j][2][i][1]) - (q_list[3]-q_list[4])*(p_list[j][2][i-1][0]-p_list[j][2][i][0]))  != 0:
                t=((q_list[2]-p_list[j][2][i-1][0]) * (p_list[j][2][i-1][1]-p_list[j][2][i][1]) - (q_list[3]-p_list[j][2][i-1][1]) * (p_list[j][2][i-1][0]-p_list[j][2][i][0]))  /  ((q_list[2]-q_list[2]) * (p_list[j][2][i-1][1]-p_list[j][2][i][1]) - (q_list[3]-q_list[4])*(p_list[j][2][i-1][0]-p_list[j][2][i][0]))                                      
                u=((q_list[2]-p_list[j][2][i-1][0]) * (q_list[3]-q_list[4]) - (q_list[3]-p_list[j][2][i-1][1]) * (q_list[2]-q_list[2]))  /  ((q_list[2]-q_list[2]) * (p_list[j][2][i-1][1]-p_list[j][2][i][1]) - (q_list[3]-q_list[4]) * (p_list[j][2][i-1][0]-p_list[j][2][i][0]))                                      
            
     
            if (t>=0 and t<=1) and (u>=0 and u<=1):
                return p_list[j][0]

            
            ### Third Case
            if  ((q_list[1]-q_list[2]) * (p_list[j][2][i-1][1]-p_list[j][2][i][1]) - (q_list[3]-q_list[3]) * (p_list[j][2][i-1][0]-p_list[j][2][i][0])) != 0:
                t=((q_list[1]-p_list[j][2][i-1][0]) * (p_list[j][2][i-1][1]-p_list[j][2][i][1]) - (q_list[3]-p_list[j][2][i-1][1]) * (p_list[j][2][i-1][0]-p_list[j][2][i][0]))  /  ((q_list[1]-q_list[2]) * (p_list[j][2][i-1][1]-p_list[j][2][i][1]) - (q_list[3]-q_list[3]) * (p_list[j][2][i-1][0]-p_list[j][2][i][0]))                                      
                u=((q_list[1]-p_list[j][2][i-1][0]) * (q_list[3]-q_list[3]) - (q_list[3]-p_list[j][2][i-1][1]) * (q_list[1]-q_list[2]))  /  ((q_list[1]-q_list[2]) * (p_list[j][2][i-1][1]-p_list[j][2][i][1]) - (q_list[3]-q_list[3]) * (p_list[j][2][i-1][0]-p_list[j][2][i][0]))                                      
            

            if (t>=0 and t<=1) and (u>=0 and u<=1):
                return p_list[j][0]


            ### Fourth Case
            if  ((q_list[1]-q_list[2]) * (p_list[j][2][i-1][1]-p_list[j][2][i][1]) - (q_list[4]-q_list[4]) * (p_list[j][2][i-1][0]-p_list[j][2][i][0])) != 0:
                t=((q_list[1]-p_list[j][2][i-1][0]) * (p_list[j][2][i-1][1]-p_list[j][2][i][1]) - (q_list[4]-p_list[j][2][i-1][1]) * (p_list[j][2][i-1][0]-p_list[j][2][i][0]))  /  ((q_list[1]-q_list[2]) * (p_list[j][2][i-1][1]-p_list[j][2][i][1]) - (q_list[4]-q_list[4]) * (p_list[j][2][i-1][0]-p_list[j][2][i][0]))                                      
                u=((q_list[1]-p_list[j][2][i-1][0]) * (q_list[4]-q_list[4]) - (q_list[4]-p_list[j][2][i-1][1]) * (q_list[1]-q_list[2]))  /  ((q_list[1]-q_list[2]) * (p_list[j][2][i-1][1]-p_list[j][2][i][1]) - (q_list[4]-q_list[4]) * (p_list[j][2][i-1][0]-p_list[j][2][i][0]))                                      
            

            if (t>=0 and t<=1) and (u>=0 and u<=1):
                return p_list[j][0]
        
    
    return 


### Function to remove the ID of the linestrings that are not in the el_list
def remove_elements(id_list,el_list):
    i=0
    while i<len(id_list):
        if id_list[i] not in el_list:
            id_list.remove(id_list[i])
        else:
            i+=1

    return id_list



###### MAIN #####
cell_list=[]      ###  A list that will contain the 4th column of the grid.dir file 

with open('grid.dir','r') as dir:
    dir_reader=dir.readlines()


#### Make a list from grid.dir ####
finished_directory_list=create_directory_list(dir_reader)


for i in range(len(finished_directory_list)):
    cell_list.append(finished_directory_list[i][3])    #### Make a list that will work as a counter for the window_check_id



####  To make the grid  ####
Min_and_Max=dir_reader[0].split(' ')
Min_and_Max[4]=Min_and_Max[4].replace('\n','')

minX=float(Min_and_Max[1])
maxX=float(Min_and_Max[2])
minY=float(Min_and_Max[3])
maxY=float(Min_and_Max[4])

Xaxis,Yaxis=grid_maker(maxX,minX,maxY,minY)



#### Make a list from grid.grd ####

with open('grid.grd','r') as grd:
    grd_reader=grd.readlines()

finished_grid_list=create_grid_list(grd_reader)


ID_list,MBR_list=find_MBRandID(finished_grid_list)


####  Make a list from querries.txt  ####

querry_list=[]

with open('queries.txt','r') as s:
    querry_reader=s.readlines()
    for row in querry_reader:
        row=row.replace('\n','')
        row=row.replace(',',' ')
        querry_list.append(row)


for i in range(len(querry_list)):
    querry_list[i]=querry_list[i].split(' ')

    for j in range(1,len(querry_list[i])):
            querry_list[i][j]=float(querry_list[i][j])


 #### Make a list with all the ID and cells that were seen by the querries
finished_cell_counter_list,finished_idlist=find_cell(finished_directory_list,cell_list,querry_list,Xaxis,Yaxis,MBR_list,ID_list)

### finished_cell_counter_list is a list with all the cells that the window sees
### finished_idlist is a list with all the ID from the linesting that are inside the cells from finished_cell_counter_list


# third part

### The finished_grid_list will contain the lines from grid.grd that their ID match with the ID of the finished_idlist
finished_grid_list=create_grid_list_with_ids(finished_idlist,finished_grid_list)


for i in range(len(finished_grid_list)):

    ID_list,MBR_list=find_MBRandID(finished_grid_list[i])

    elements_to_keep=check_axis(querry_list[i],MBR_list,finished_idlist[i],finished_grid_list[i])     ### Create a list with the elements that will stay after checking the xand y axis the lines individually
    finished_idlist[i]=remove_elements(finished_idlist[i],elements_to_keep)                                              ### Remove the other elements


            
### Print final product
for i in range(0,len(finished_idlist)):
    print("Querry",i+1,"results:")
    print(finished_idlist[i])
    print("cells:",len(finished_cell_counter_list[i]))
    print("results:",len(finished_idlist[i]))
    print("\n")
