import toml

def readToml():
   tomlFile = "../setup/monan_setup.toml"
   data=toml.load(tomlFile)
   
   paths = data["paths"]
   defines = data["defines"]
   compiler = data["compiler"]
   model = data["model"]

   MPAS = True
   DO_PHYSICS = False
   MPAS_OPENMP = False
   MPAS_OPENACC = False
   MPAS_PIO_SUPPORT = False
   MPAS_DEBUG = False
   USE_PIO2 = False
   CONST_INNER_DIMS = False
   MPAS_CAM_DYCORE = False

   registry = paths["REGISTRY"]

   netcdf_dir =compiler["NETCDF_DIR"]
   hdf5_dir   =compiler["HDF5_DIR"]
   pnetcdf_dir=compiler["PNETCDF_DIR"]
   mpi_dir    =compiler["MPI_DIR"]
   pio_dir    =compiler["PIO_DIR"]
   f90_compiler =compiler["F90"]
   cc_compiler = compiler["CC"]
   mpif90 = compiler["MPIF90"]
   mpicc = compiler["MPICC"]
   fflags = compiler["FFLAGS"]
   cflags = compiler["CFLAGS"]
   libs = compiler["LIBS"]

   pp_command = " "
   if defines["MPAS"] == "YES":
      MPAS = True
      pp_command = pp_command+"-Dmpas "
   if defines["_MPI"] == "YES":
      _MPI = True
      pp_command = pp_command+"-D_MPI "
   if defines["CORE_ATMOSPHERE"] == "YES":
      CORE_ATMOSPHERE = True
      pp_command = pp_command+"-DCORE_ATMOSPHERE "
   if defines["DO_PHYSICS"] == "YES":
      DO_PHYSICS = True
      pp_command = pp_command+"-DDO_PHYSICS "
   if defines["MPAS_OPENMP"] == "YES":
      MPAS_OPENMP = True
      pp_command = pp_command+"-DMPAS_OPENMP "
   if defines["MPAS_OPENMP"] == "YES":
      MPAS_OPENACC = True
      pp_command = pp_command+"-DMPAS_OPENACC "
   if defines["MPAS_PIO_SUPPORT"] == "YES":
      MPAS_PIO_SUPPORT = True
      pp_command = pp_command+"-DMPAS_PIO_SUPPORT "
   if defines["MPAS_SMIOL_SUPPORT"] == "YES":
      MPAS_SMIOL_SUPPORT = True
      pp_command = pp_command+"-DMPAS_SMIOL_SUPPORT "
   if defines["MPAS_DEBUG"] == "YES":
      MPAS_DEBUG = True
      pp_command = pp_command+"-DMPAS_DEBUG "
   if defines["USE_PIO2"] == "YES":
      USE_PIO2 = True   
      pp_command = pp_command+"-DUSE_PIO2 "
   if defines["CONST_INNER_DIMS"] == "YES":
      CONST_INNER_DIMS = True      
      pp_command = pp_command+"-DCONST_INNER_DIMS "
   if defines["MPAS_CAM_DYCORE"] == "YES":
      MPAS_CAM_DYCORE = True
      pp_command = pp_command+"-DMPAS_CAM_DYCORE "
   if defines["WRF_DFI_RADAR"] == "YES":
      pp_command = pp_command+"-DWRF_DFI_RADAR=1 "
   else:
      pp_command = pp_command+"-DWRF_DFI_RADAR=0 "

   if defines["WRF_CHEM"] == "YES":
      pp_command = pp_command+"-DWRF_CHEM=1 "
   else:
      pp_command = pp_command+"-DWRF_CHEM=0 "

   if defines["HWRF"] == "YES":
      pp_command = pp_command+"-DHWRF=1 "
   else:
      pp_command = pp_command+"-DHWRF=0 "

   if defines["EM_CORE"] == "YES":
      pp_command = pp_command+"-DEM_CORE=1 "
   else:
      pp_command = pp_command+"-DEM_CORE=0 "

   if defines["NMM_CORE"] == "YES":
      pp_command = pp_command+"-DNMM_CORE=1 "
   else:
      pp_command = pp_command+"-DNMM_CORE=0 "

   version = model["VERSION"]

   fpm_command = 'fpm build compiler="'
   fpm_command = fpm_command + mpif90 + '" --flag "'+fflags + '" --flag "'  + libs + '" --flag "' + pp_command + '" '
   fpm_command = fpm_command + '--c-compiler="' + mpicc + '" --c-flag "' + cflags +'"'

   return pp_command,version,registry,netcdf_dir,hdf5_dir,pnetcdf_dir,mpi_dir,pio_dir,fpm_command    