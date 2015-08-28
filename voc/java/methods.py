from .constants import Utf8
from .attributes import Attribute

# From: http://docs.oracle.com/javase/specs/jvms/se7/html/jvms-4.html


##########################################################################
# 4.6. Methods
##########################################################################

# Each method, including each instance initialization method (§2.9) and the
# class or interface initialization method (§2.9), is described by a method_info
# structure. No two methods in one class file may have the same name and
# descriptor (§4.3.3).

class Method:
    # u2 access_flags;
    # u2 name_index;
    # u2 descriptor_index;
    # u2 attributes_count;
    # attribute_info attributes[attributes_count];

    # Table 4.5. Method access and property flags

    ACC_PUBLIC = 0x0001         # Declared public; may be accessed from outside its package.
    ACC_PRIVATE = 0x0002        # Declared private; accessible only within the defining class.
    ACC_PROTECTED = 0x0004      # Declared protected; may be accessed within subclasses.
    ACC_STATIC = 0x0008         # Declared static.
    ACC_FINAL = 0x0010          # Declared final; must not be overridden (§5.4.5).
    ACC_SYNCHRONIZED = 0x0020   # Declared synchronized; invocation is wrapped by a monitor use.
    ACC_BRIDGE = 0x0040         # A bridge method, generated by the compiler.
    ACC_VARARGS = 0x0080        # Declared with variable number of arguments.
    ACC_NATIVE = 0x0100         # Declared native; implemented in a language other than Java.
    ACC_ABSTRACT = 0x0400       # Declared abstract; no implementation is provided.
    ACC_STRICT = 0x0800         # Declared strictfp; floating-point mode is FP-strict.
    ACC_SYNTHETIC = 0x1000      # Declared synthetic; not present in the source code.

    def __init__(
                self, name, descriptor,
                public=True, private=False, protected=False, static=False,
                final=False, synchronized=False, bridge=False, varargs=False,
                native=False, abstract=False, strict=False, synthetic=False,
                attributes=None
            ):

        # The value of the name_index item must be a valid index into the
        # constant_pool table. The constant_pool entry at that index must be a
        # CONSTANT_Utf8_info (§4.4.7) structure representing either one of the
        # special method names (§2.9) <init> or <clinit>, or a valid unqualified
        # name (§4.2.2) denoting a method.
        self.name = Utf8(name)

        # The value of the descriptor_index item must be a valid index into the
        # constant_pool table. The constant_pool entry at that index must be a
        # CONSTANT_Utf8_info (§4.4.7) structure representing a valid method
        # descriptor (§4.3.3).

        # A future edition of this specification may require that the last
        # parameter descriptor of the method descriptor is an array type if the
        # ACC_VARARGS flag is set in the access_flags item.
        self.descriptor = Utf8(descriptor)

        # The ACC_VARARGS flag indicates that this method takes a variable
        # number of arguments at the source code level. A method declared to
        # take a variable number of arguments must be compiled with the
        # ACC_VARARGS flag set to 1. All other methods must be compiled with the
        # ACC_VARARGS flag set to 0.

        # The ACC_BRIDGE flag is used to indicate a bridge method generated by a
        # Java compiler.

        # A method may be marked with the ACC_SYNTHETIC flag to indicate that it
        # was generated by a compiler and does not appear in source code, unless
        # it is one of the methods named in §4.7.8.

        # Methods of classes may set any of the flags in Table 4.5. However, a
        # specific method of a class may have at most one of its ACC_PRIVATE,
        # ACC_PROTECTED and ACC_PUBLIC flags set (JLS §8.4.3). If a specific
        # method has its ACC_ABSTRACT flag set, it must not have any of its
        # ACC_FINAL, ACC_NATIVE, ACC_PRIVATE, ACC_STATIC, ACC_STRICT or
        # ACC_SYNCHRONIZED flags set (JLS §8.4.3.1, JLS §8.4.3.3, JLS §8.4.3.4).

        # All interface methods must have their ACC_ABSTRACT and ACC_PUBLIC
        # flags set; they may have their ACC_VARARGS, ACC_BRIDGE and
        # ACC_SYNTHETIC flags set and must not have any of the other flags in
        # Table 4.5 set (JLS §9.4).

        self.private = private
        if self.private:
            self.protected = False
            self.public = False
        else:
            self.protected = protected
            if self.protected:
                self.public = False
            else:
                self.public = True

        self.static = static
        self.final = final
        self.synchronized = synchronized
        self.bridge = bridge
        self.varargs = varargs
        self.native = native
        self.abstract = abstract
        self.strict = strict
        self.synthetic = synthetic

        # Each value of the attributes table must be an attribute structure
        # (§4.7). A method can have any number of optional attributes associated
        # with it.

        # The attributes defined by this specification as appearing in the
        # attributes table of a method_info structure are the Code (§4.7.3),
        # Exceptions (§4.7.5), Synthetic (§4.7.8), Signature (§4.7.9),
        # Deprecated (§4.7.15), RuntimeVisibleAnnotations (§4.7.16),
        # RuntimeInvisibleAnnotations (§4.7.17),
        # RuntimeVisibleParameterAnnotations (§4.7.18),
        # RuntimeInvisibleParameterAnnotations (§4.7.19), and AnnotationDefault
        # (§4.7.20) attributes.

        # A Java Virtual Machine implementation must recognize and correctly
        # read Code (§4.7.3) and Exceptions (§4.7.5) attributes found in the
        # attributes table of a method_info structure. If a Java Virtual Machine
        # implementation recognizes class files whose version number is 49.0 or
        # above, it must recognize and correctly read Signature (§4.7.9),
        # RuntimeVisibleAnnotations (§4.7.16), RuntimeInvisibleAnnotations
        # (§4.7.17), RuntimeVisibleParameterAnnotations (§4.7.18),
        # RuntimeInvisibleParameterAnnotations (§4.7.19) and AnnotationDefault
        # (§4.7.20) attributes found in the attributes table of a method_info
        # structure of a class file whose version number is 49.0 or above.

        # A Java Virtual Machine implementation is required to silently ignore
        # any or all attributes in the attributes table of a method_info
        # structure that it does not recognize. Attributes not defined in this
        # specification are not allowed to affect the semantics of the class
        # file, but only to provide additional descriptive information (§4.7.1).
        self.attributes = attributes if attributes else []

    def __repr__(self):
        return '<Method access:0x%04x name:%s, descriptor:%s>' % (self.access_flags, self.name, self.descriptor)

    @staticmethod
    def read(reader, dump=None):
        access_flags = reader.read_u2()

        name = reader.constant_pool[reader.read_u2()].bytes.decode('utf8')
        descriptor = reader.constant_pool[reader.read_u2()].bytes.decode('utf8')
        attributes_count = reader.read_u2()

        if dump:
            print("    " * dump, 'Method %s %s' % (name, descriptor))

            access_description = ', '.join(f for f in [
                    flag if access_flags & mask else None
                    for flag, mask in [
                        ('public', Method.ACC_PUBLIC),
                        ('private', Method.ACC_PRIVATE),
                        ('protected', Method.ACC_PROTECTED),
                        ('static', Method.ACC_STATIC),
                        ('final', Method.ACC_FINAL),
                        ('synchronized', Method.ACC_SYNCHRONIZED),
                        ('bridge', Method.ACC_BRIDGE),
                        ('varargs', Method.ACC_VARARGS),
                        ('native', Method.ACC_NATIVE),
                        ('abstract', Method.ACC_ABSTRACT),
                        ('strict', Method.ACC_STRICT),
                        ('synthetic', Method.ACC_SYNTHETIC),
                    ]
                ] if f)
            print("    " * dump, '    Flags: 0x%04x%s' % (access_flags, ' (%s)') % access_description if access_description else '')

            print("    " * dump, '    Attributes: (%s)' % attributes_count)

        attributes = []
        for i in range(0, attributes_count):
            attributes.append(
                Attribute.read(reader, dump=dump + 2 if dump is not None else dump)
            )

        return Method(
            name=name,
            descriptor=descriptor,
            public=bool(access_flags & Method.ACC_PUBLIC),
            private=bool(access_flags & Method.ACC_PRIVATE),
            protected=bool(access_flags & Method.ACC_PROTECTED),
            static=bool(access_flags & Method.ACC_STATIC),
            final=bool(access_flags & Method.ACC_FINAL),
            synchronized=bool(access_flags & Method.ACC_SYNCHRONIZED),
            bridge=bool(access_flags & Method.ACC_BRIDGE),
            varargs=bool(access_flags & Method.ACC_VARARGS),
            native=bool(access_flags & Method.ACC_NATIVE),
            abstract=bool(access_flags & Method.ACC_ABSTRACT),
            strict=bool(access_flags & Method.ACC_STRICT),
            synthetic=bool(access_flags & Method.ACC_SYNTHETIC),
            attributes=attributes,
        )

    def write(self, writer):
        writer.write_u2(self.access_flags)
        writer.write_u2(writer.constant_pool.index(self.name))
        writer.write_u2(writer.constant_pool.index(self.descriptor))
        writer.write_u2(self.attributes_count)

        for attribute in self.attributes:
            attribute.write(writer)

    def resolve(self, constant_pool):
        constant_pool.add(self.name)
        constant_pool.add(self.descriptor)

        for attribute in self.attributes:
            attribute.resolve(constant_pool)

    @property
    def attributes_count(self):
        return len(self.attributes)

    @property
    def access_flags(self):
        """A specific instance initialization method (§2.9) may have at most one
        of its ACC_PRIVATE, ACC_PROTECTED, and ACC_PUBLIC flags set, and may
        also have its ACC_STRICT, ACC_VARARGS and ACC_SYNTHETIC flags set, but
        must not have any of the other flags in Table 4.5 set.

        Class and interface initialization methods (§2.9) are called
        implicitly by the Java Virtual Machine. The value of their
        access_flags item is ignored except for the setting of the ACC_STRICT
        flag.

        All bits of the access_flags item not assigned in Table 4.5 are
        reserved for future use. They should be set to zero in generated class
        files and should be ignored by Java Virtual Machine implementations.
        """
        return (
            (self.ACC_PUBLIC if self.public else 0) |
            (self.ACC_PRIVATE if self.private else 0) |
            (self.ACC_PROTECTED if self.protected else 0) |
            (self.ACC_STATIC if self.static else 0) |
            (self.ACC_FINAL if self.final else 0) |
            (self.ACC_SYNCHRONIZED if self.synchronized else 0) |
            (self.ACC_BRIDGE if self.bridge else 0) |
            (self.ACC_VARARGS if self.varargs else 0) |
            (self.ACC_NATIVE if self.native else 0) |
            (self.ACC_ABSTRACT if self.abstract else 0) |
            (self.ACC_STRICT if self.strict else 0) |
            (self.ACC_SYNTHETIC if self.synthetic else 0)
        )
