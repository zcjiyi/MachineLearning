############################################################################
# LGPL License                                                             #
#                                                                          #
# This file is part of the Machine Learning Framework.                     #
# Copyright (c) 2010, Philipp Kraus, <philipp.kraus@flashpixx.de>          #
# This program is free software: you can redistribute it and/or modify     #
# it under the terms of the GNU Lesser General Public License as           #
# published by the Free Software Foundation, either version 3 of the       #
# License, or (at your option) any later version.                          #
#                                                                          #
# This program is distributed in the hope that it will be useful,          #
# but WITHOUT ANY WARRANTY; without even the implied warranty of           #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
# GNU Lesser General Public License for more details.                      #
#                                                                          #
# You should have received a copy of the GNU Lesser General Public License #
# along with this program. If not, see <http://www.gnu.org/licenses/>.     #
############################################################################

# -*- coding: utf-8 -*-
import os
import urllib2
import re
import shutil
import subprocess
import glob
Import("*")


#=== help function ===================================================================================================================
def runsyscmd(cmd, env) :
    ret = subprocess.call( cmd, shell=True )
    if ret <> 0 and not(env["skipbuilderror"]) :
        print "\nan error occurred during building"
        res = ""
        while res != "a" and res != "c" :
            res = raw_input("(a)bort or (c)ontinue: ")
            if res == "a" :
                sys.exit(1)
        
                        
def downloadfile(url, file)  :
    if os.path.isfile(file) :
        return
                
    target = open( file, "w" )
    f = urllib2.urlopen(url)
    target.write(f.read())
    target.close()
    f.close()
    
    
def clearbuilddir(target, source, env) :
    clearlist = []
    for i in os.listdir("install") :
        if os.path.isfile(os.path.join("install", i)) :
            continue
        if i <> "build" :
            clearlist.append(i)
    
    for i in clearlist :
        for pathentry in os.walk(os.path.join("install", i), False):
            for dir in pathentry[1]:
                path = os.path.join(pathentry[0], dir)
                if os.path.islink(path):
                    os.unlink(path)
                else:
                    os.rmdir(path)

            for file in pathentry[2]:
                path = os.path.join(pathentry[0], file)
                os.unlink(path)
       
        os.removedirs(os.path.join("install", i))
    
    return []



#=== download packages ===============================================================================================================
def download_boost(target, source, env)  :
    # read download path of the Boost (latest version)
    f = urllib2.urlopen("http://www.boost.org/users/download/")
    html = f.read()
    f.close()
    
    found = re.search("<a href=\"http://sourceforge.net/projects/boost/files/(.*)\">Download</a>", html)
    if found == None :
        raise RuntimeError("Boost Download URL not found")
        
    downloadurl = found.group(0)
    downloadurl = downloadurl.replace("<a href=\"", "")
    downloadurl = downloadurl.replace("\">Download</a>", "")
    
    # read url of the tar.bz2
    f = urllib2.urlopen(downloadurl)
    html = f.read()
    f.close()

    found = re.search("<a href=\"http://sourceforge.net/projects/boost/files/boost(.*).tar.bz2/download", html)
    if found == None :
        raise RuntimeError("Boost Download URL not found")

    downloadurl = found.group(0)
    downloadurl = downloadurl.replace("<a href=\"", "")

    downloadfile(downloadurl, os.path.join("install", "boost.tar.bz2"))
    return []


def download_hdf(target, source, env) :
    # read download path of the HDF
    f = urllib2.urlopen("http://www.hdfgroup.org/ftp/HDF5/current/src/")
    html = f.read()
    f.close()
    
    found = re.search("<a href=\"(.*)tar.bz2\">", html)
    if found == None :
        raise RuntimeError("HDF Download URL not found")
    downloadurl = found.group(0)

    downloadurl = downloadurl.replace("<a href=\"", "")
    downloadurl = downloadurl.replace("\">", "")
    downloadurl = "http://www.hdfgroup.org/ftp/HDF5/current/src/" + downloadurl

    # download the package
    downloadfile(downloadurl, os.path.join("install", "hdf.tar.bz2"))
    return []


def download_atlaslapack(target, source, env) :
    # read download path of the LAPack (latest version)
    f = urllib2.urlopen("http://www.netlib.org/lapack/")
    html = f.read()
    f.close()
    
    found = re.search("<a href=\"http://www.netlib.org/lapack/(.*)tgz\">", html)
    if found == None :
        raise RuntimeError("LAPack Download URL not found")
        
    downloadurl = found.group(0)
    downloadurl = downloadurl.replace("<a href=\"", "")
    downloadurl = downloadurl.replace("\">", "")
    
    downloadfile(downloadurl, os.path.join("install", "lapack.tgz"))
    downloadfile("http://sourceforge.net/projects/math-atlas/files/latest/download?source=files", os.path.join("install", "atlas.tar.bz2"))
    
    # extract ATLAS tar here, because errors are ignored
    os.system("tar xfvj "+os.path.join("install", "atlas.tar.bz2")+" -C install")
    
    return []


def download_ginaccln(target, source, env) :
    # read download path of the GiNaC (latest version)
    f = urllib2.urlopen("http://www.ginac.de/Download.html")
    html = f.read()
    f.close()
    
    found = re.search("<a href=\"http://www.ginac.de/(.*).tar.bz2\">this link</a>", html)
    if found == None :
        raise RuntimeError("GiNaC Download URL not found")
    
    downloadurl = found.group(0)
    downloadurl = downloadurl.replace("<a href=\"", "")
    downloadurl = downloadurl.replace("\">this link</a>", "")
    
    downloadfile(downloadurl, os.path.join("install", "ginac.tar.bz2"))

    
    # read download path of the CLN (latest version)
    f = urllib2.urlopen("http://www.ginac.de/CLN/")
    html = f.read()
    f.close()
    
    found = re.search("<a href=\"(.*).tar.bz2\">from here</a>", html)
    if found == None :
        raise RuntimeError("CLN Download URL not found")
    
    downloadurl = found.group(0)
    downloadurl = downloadurl.replace("<a href=\"", "")
    downloadurl = "http://www.ginac.de/CLN/" + downloadurl.replace("\">from here</a>", "")
    
    downloadfile(downloadurl, os.path.join("install", "cln.tar.bz2"))
    return []


def download_jsoncpp(target, source, env) :
    downloadfile("http://sourceforge.net/projects/jsoncpp/files/latest/download?source=files", os.path.join("install", "jsoncpp.tar.gz"))
    return []


#=== building libraries ==============================================================================================================
def build_boost(target, source, env)  :
    boostpath = glob.glob(os.path.join("install", "boost_*"))
    if boostpath == None or not(boostpath) :
        raise RuntimeError("Boost Build Directory not found")

    boostpath     = boostpath[0]
    
    # extract the version part
    boostversion  = boostpath.replace(os.path.join("install", "boost_"), "")
    boostversion  = boostversion.replace("_", ".")

    # for calling bootstrap.sh change the current work directory
    runsyscmd("cd "+boostpath+"; ./bootstrap.sh", env)
    
    # call the bjam command
    toolset = "gcc"
    if env["PLATFORM"].lower() == "darwin" :
        toolset = "darwin"
        
    # if MPI is set, compile Boost with MPI support
    mpi = ""
    if env["withmpi"] :
        oFile = open(os.path.join(boostpath, "tools", "build", "v2", "user-config.jam"), "a+")
        oFile.write("\n using mpi ;\n")
        oFile.close()
        mpi = "--with-mpi"
            
    # build the Boost
    runsyscmd("cd "+boostpath+"; ./b2 "+mpi+" --with-exception --with-filesystem --with-math --with-random --with-regex --with-date_time --with-thread --with-system --with-program_options --with-serialization --with-iostreams --disable-filesystem2 threading=multi runtime-link=shared variant=release toolset="+toolset+" install --prefix="+os.path.abspath(os.path.join(os.curdir, "install", "build", "boost", boostversion)), env)

    # checkout the numerical binding
    runsyscmd("svn checkout http://svn.boost.org/svn/boost/sandbox/numeric_bindings/ "+os.path.join("install", "build", "boost", "sandbox", "numeric_bindings"), env )

    return []
    
    
def build_hdf(target, source, env) :
    hdfpath = glob.glob(os.path.join("install", "hdf?-*"))
    if hdfpath == None or not(hdfpath) :
        raise RuntimeError("HDF Build Directory not found")

    hdfpath     = hdfpath[0]
    hdfversion  = hdfpath.replace(os.path.join("install", "hdf"), "")

    runsyscmd( "cd "+hdfpath+"; ./configure --enable-cxx --prefix="+os.path.abspath(os.path.join("install", "build", "hdf", hdfversion))+ "; make; make install", env )
    return []
    

def build_atlaslapack(target, source, env) :
    f = urllib2.urlopen("http://sourceforge.net/projects/math-atlas/files/")
    html = f.read()
    f.close()

    found = re.search("<small title=\"(.*)tar.bz2\">(.*)</small>", html)
    if found == None :
        raise RuntimeError("ATLAS Version can not be detected")

    atlasversion = found.group(2)
    atlasversion = atlasversion.replace("atlas", "")
    atlasversion = atlasversion.replace(".tar.bz2", "")

    ptrwidth = ""
    if env["atlaspointerwidth"] == "32" :
        ptrwidth = "-b 32"
    elif env["atlaspointerwidth"] == "64" :
        ptrwidth = "-b 64"

    cputhrottle = ""
    if not(env["atlascputhrottle"]) :
        cputhrottle = "-Si cputhrchk 0"
    
    runsyscmd( "cd "+os.path.join("install", "atlasbuild")+"; ../ATLAS/configure --dylibs "+ptrwidth+" "+cputhrottle+" --with-netlib-lapack-tarfile=../lapack.tgz --prefix="+os.path.abspath(os.path.join("install", "build", "atlas", atlasversion))+ "; make", env )
    return []
    
    
def soname_atlaslapack(target, source, env) :
    oFile = open( os.path.join("install", "atlasbuild", "lib", "Makefile"), "r" )
    makefile = oFile.read()
    oFile.close()
    
    makefile = makefile.replace("(LD) $(LDFLAGS) -shared -soname $(LIBINSTdir)/$(outso) -o $(outso)", "(LD) $(LDFLAGS) -shared -soname $(outso) -o $(outso)")

    oFile = open( os.path.join(os.curdir, "install", "atlasbuild", "lib", "Makefile"), "w" )
    oFile.write(makefile)
    oFile.close()

    return []


def install_atlaslapack(target, source, env) :
    runsyscmd( "cd "+os.path.join("install", "atlasbuild")+"; make shared; make install", env )
    return []
    
    
def build_ginaccln(target, source, env) :
    clnpath = glob.glob(os.path.join("install", "cln-*"))
    if clnpath == None or not(clnpath) :
        raise RuntimeError("CLN Build Directory not found")
    
    clnpath     = clnpath[0]
    clnversion  = clnpath.replace(os.path.join("install", "cln-"), "")
    
    ginacpath = glob.glob(os.path.join("install", "ginac-*"))
    if ginacpath == None or not(ginacpath) :
        raise RuntimeError("GiNaC Build Directory not found")
    
    ginacpath     = ginacpath[0]
    ginacversion  = ginacpath.replace(os.path.join("install", "ginac-"), "")

    runsyscmd( "cd "+clnpath+"; ./configure --prefix="+os.path.abspath(os.path.join("install", "build", "cln", clnversion))+ "; make; make install", env )
    runsyscmd( "cd "+ginacpath+"; export CLN_CFLAGS=-I"+os.path.abspath(os.path.join("install", "build", "cln", clnversion, "include"))+"; export CLN_LIBS=\"-L"+os.path.abspath(os.path.join("install", "build", "cln", clnversion, "lib"))+" -lcln\"; ./configure --prefix="+os.path.abspath(os.path.join("install", "build", "ginac", ginacversion))+ "; make; make install", env )
    return []


def build_jsoncpp(target, source, env) :
    jsonpath = glob.glob(os.path.join("install", "jsoncpp-src-*"))
    if jsonpath == None or not(jsonpath) :
        raise RuntimeError("JSON CPP Build Directory not found")

    jsonpath     = jsonpath[0]
    jsonversion  = jsonpath.replace(os.path.join("install", "jsoncpp-src-"), "")
    
    runsyscmd("cd "+jsonpath+"; scons platform=linux-gcc", env)
    
    # manual copy of the data
    try :
        os.makedirs(os.path.join("install", "build", "jsoncpp", jsonversion))
    except :
        pass
    try :
        os.makedirs(os.path.join("install", "build", "jsoncpp", jsonversion, "lib"))
    except :
        pass
    try :
        shutil.copytree(os.path.join(jsonpath, "include"), os.path.join("install", "build", "jsoncpp", jsonversion, "include"))
    except :
        pass

    files = []
    files.extend( glob.glob(os.path.join(jsonpath, "libs", "**", "*"+env["SHLIBSUFFIX"])) )
    files.extend( glob.glob(os.path.join(jsonpath, "libs", "**", "*"+env["LIBSUFFIX"])) )
    installpath = os.path.join("install", "build", "jsoncpp", jsonversion, "lib")
    for i in files :
        filename =os.path.split(i)[-1]
        shutil.copy(i, os.path.join(installpath, filename))
        os.symlink(os.path.join("./", filename), os.path.join(installpath, "libjson" + os.path.splitext(filename)[1]))

    return []


#=== target structure ================================================================================================================
skiplist = str(env["skipbuild"]).split(",")
if ("librarybuild" in COMMAND_LINE_TARGETS) and ("all" in skiplist) :
    raise RuntimeError("nothing to build")

#build into a temp dir
lst = []
lst.append( env.Command("mkinstalldir", "", Mkdir("install")) )
lst.append( env.Command("mkbuilddir", "", Mkdir(os.path.join("install", "build"))) )

#clear install directories before compiling
lst.append( env.Command("cleanbeforebuilddir", "", clearbuilddir) )

#download LAPack & ATLAS, extract & install
if not("atlas" in skiplist) :
    lst.append( env.Command("downloadlapackatlas", "", download_atlaslapack) )
    lst.append( env.Command("mkatlasbuilddir", "", Mkdir(os.path.join("install", "atlasbuild"))) )
    lst.append( env.Command("buildatlaslapack", "", build_atlaslapack) )
    if env['PLATFORM'].lower() == "posix" or env['PLATFORM'].lower() == "cygwin" :
        lst.append( env.Command("sonameatlaslapack", "", soname_atlaslapack) )
    lst.append( env.Command("installatlaslapack", "", install_atlaslapack) )

# download Boost, extract & install
if not("boost" in skiplist) :
    lst.append( env.Command("downloadboost", "", download_boost) )
    lst.append( env.Command("extractboost", "", "tar xfvj "+os.path.join("install", "boost.tar.bz2")+" -C install") )
    lst.append( env.Command("buildboost", "", build_boost) )

# download HDF, extract & install
if not("hdf" in skiplist) :
    lst.append( env.Command("downloadhdf", "", download_hdf) )
    lst.append( env.Command("extracthdf", "", "tar xfvj "+os.path.join("install", "hdf.tar.bz2")+" -C install") )
    lst.append( env.Command("buildhdf", "", build_hdf) )

#download GiNaC & CLN, extract & install
if not("ginac" in skiplist) :
    lst.append( env.Command("downloadginaccln", "", download_ginaccln) )
    lst.append( env.Command("extractginac", "", "tar xfvj "+os.path.join("install", "ginac.tar.bz2")+" -C install") )
    lst.append( env.Command("extractcln", "", "tar xfvj "+os.path.join("install", "cln.tar.bz2")+" -C install") )
    lst.append( env.Command("buildginaccln", "", build_ginaccln) )

#download JSON library, extract & install
if not("json" in skiplist) :
    lst.append( env.Command("downloadjsoncpp", "", download_jsoncpp) )
    lst.append( env.Command("extractjsoncpp", "", "tar xfvz "+os.path.join("install", "jsoncpp.tar.gz")+" -C install") )
    lst.append( env.Command("buildjsoncpp", "", build_jsoncpp) )

#clear install directories after compiling
lst.append( env.Command("cleanafterbuilddir", "", clearbuilddir) )

env.Alias("librarybuild", lst)





