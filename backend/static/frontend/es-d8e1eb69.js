var accountSettings = {
	contactTitle: "Contáctanos",
	emailButton: "Correo",
	whatsappButton: "WhatsApp",
	activeStatus: "Tu cuenta está activa",
	cancelAccountButton: "Cancelar cuenta",
	cancellingButton: "Cancelando...",
	notAuthenticatedStatus: "No estás autenticado",
	createAccountButton: "Crear cuenta",
	expiredStatus: "Tu suscripción ha expirado",
	activateButton: "Activar cuenta",
	activatingButton: "Activando...",
	errorMessage: "Ocurrió un error al obtener la información de la cuenta.",
	deleteAccount: {
		confirmMessage: "¿Estás seguro de que quieres eliminar tu cuenta? Esta acción no se puede deshacer.",
		button: "Eliminar cuenta"
	}
};
var nav = {
	dashboard: "Panel",
	upload: "Subir",
	logout: "CERRAR SESIÓN",
	pricing: "Precios",
	login: "Iniciar sesión",
	startNow: "Empezar ahora",
	accountSettings: "Ajustes de la cuenta",
	aiBusiness: "Soluciones de IA"
};
var footer = {
	tiktok: "Tiktok",
	privacyPolicy: "Política de Privacidad",
	cookiePolicy: "Política de Cookies",
	termsOfService: "Términos de Servicio",
	copyright: "Yekar © {year}. Todos los derechos reservados.",
	legalLinks: {
		privacyPolicy: "Política de Privacidad",
		cookiePolicy: "Política de Cookies",
		termsOfService: "Términos de Servicio"
	},
	socialLinks: {
		instagram: "https://www.instagram.com/yekar_ai",
		twitter: "https://twitter.com/yekar_ai",
		youtube: "https://www.youtube.com/@yekar_ai",
		tiktok: "https://www.tiktok.com/@yekar_ai"
	}
};
var privacyPolicy = {
	title: "Política de Privacidad",
	scope: {
		title: "Ámbito de aplicación",
		p1: "Yekar se compromete a respetar la privacidad de aquellos que visiten y utilicen su sitio web alojado en la URL https://yekar.es (el 'Sitio Web').",
		p2: "La presente Política de Privacidad tiene por objeto informar a los usuarios sobre el tratamiento de los datos personales recogidos a través del Sitio Web y sus servicios asociados.",
		p3: "La utilización de https://yekar.es o de cualquiera de sus servicios asociados (como los embudos de venta) supone la aceptación por parte del usuario de las disposiciones incluidas en esta Política de Privacidad y el tratamiento de sus datos personales conforme a lo aquí establecido y de acuerdo con los usos y facultades previstos en la normativa."
	},
	purposes: {
		title: "Finalidades",
		p1: "Le informamos que los datos podrán ser tratados para facilitarle información comercial y actualizaciones sobre el sitio web y nuestros productos o servicios a través de medios electrónicos, siempre que usted autorice su tratamiento.",
		p2: "Sus datos podrán ser objeto de elaboración de perfiles para aplicar un plan de fidelización basado en la relación comercial con los usuarios y clientes y ofrecerles ofertas más adecuadas a sus preferencias.",
		p3: "Si el usuario se pone en contacto con https://yekar.es a través del sitio web, sus datos personales se utilizarán para responder a las solicitudes de información y otras consultas que haya podido realizar."
	},
	about: {
		title: "Acerca de la política de privacidad",
		p1: "Yekar está especialmente sensibilizado con la protección de los datos de los usuarios y clientes a los que se accede a través de https://yekar.es.",
		p2: "Todo ello con el fin de ofrecer un sitio web y un servicio transparentes a su comunidad y permitir que las personas que accedan al sitio web puedan decidir libre y voluntariamente qué información desean facilitar en cada momento."
	},
	videoStorage: {
		title: "Almacenamiento temporal de videos",
		p1: "Como parte de nuestro servicio, Yekar almacena temporalmente los videos subidos por los usuarios en nuestros servidores seguros. Este almacenamiento es necesario para ofrecer el servicio de visualización de videos a los usuarios durante un período limitado.",
		p2: "Los videos se almacenan por un máximo de 48 horas, tras lo cual son eliminados automáticamente de nuestros servidores. En ningún caso los videos son almacenados en otra ubicación o por un período más largo del especificado.",
		p3: "El acceso a estos videos está estrictamente limitado a los usuarios autorizados y al personal técnico necesario para el mantenimiento y funcionamiento del servicio.",
		p4: "De acuerdo con el RGPD, los usuarios tienen derecho a solicitar la eliminación de sus videos antes del período de 48 horas si así lo desean. Para ejercer este derecho, pueden ponerse en contacto con nuestro equipo de soporte a través de jon@yekar.es.",
		p5: "Yekar implementa medidas de seguridad técnicas y organizativas apropiadas para proteger los videos almacenados contra el acceso no autorizado, la pérdida o la alteración accidental."
	},
	confidentiality: {
		title: "Confidencialidad y seguridad",
		p1: "Los usuarios facilitarán sus datos y realizarán pagos a través de Yekar. Estos datos personales serán tratados con total confidencialidad.",
		p2: "Asimismo, se informa que https://yekar.es cederá los datos al responsable del evento organizado, así como a cualesquiera otros vinculados al evento, pero no a terceros sin relación o motivo justificado."
	},
	rights: {
		title: "Derechos de Acceso, Rectificación, Cancelación y Oposición",
		p1: "En cualquier momento, el usuario podrá acceder, rectificar, cancelar u oponerse al tratamiento de sus datos personales dirigiéndose a la pestaña \"Contacto\" del Sitio Web o seleccionando la opción \"darse de baja\" en cualquier correo electrónico enviado por el Sitio Web."
	},
	userRights: {
		title: "Derechos del usuario",
		p1: "El interesado de datos personales podrá ejercitar los derechos previstos en el Reglamento General de Protección de Datos y en la Ley Orgánica 3/2018 de Protección de Datos Personales y Garantías de su Tratamiento."
	},
	salesFunnels: {
		title: "Embudos de venta y publicidad",
		p1: "Yekar podrá utilizar campañas publicitarias y técnicas de venta a través de las cuales podrá solicitar determinados datos personales para la prestación del servicio solicitado."
	},
	disclaimer: {
		title: "Descargo de responsabilidad",
		p1: "La empresa no se hace responsable de las opiniones y comentarios publicados en redes sociales, páginas web, foros, reseñas o apps sobre Yekar o cualquiera de sus servicios, personal o instalaciones, siendo el autor el único responsable de su veracidad."
	},
	modification: {
		title: "Modificación de la Política de Privacidad",
		p1: "Yekar se reserva el derecho a modificar la presente política en cualquier momento con el fin de adaptarla a las novedades legislativas.",
		p2: "Para cualquier duda, consulta o comentario sobre esta política, no dude en ponerse en contacto con nosotros en support@yekar.es.",
		p3: "Esta política de privacidad está actualizada a 11 de octubre de 2024."
	}
};
var termsOfService = {
	title: "Términos de Servicio",
	acceptance: {
		title: "Aceptación de los Términos",
		p1: "Al acceder y utilizar los servicios de Yekar, usted acepta estar sujeto a estos Términos de Servicio. Si no está de acuerdo con alguna parte de estos términos, no podrá utilizar nuestros servicios."
	},
	description: {
		title: "Descripción del Servicio",
		p1: "Yekar proporciona una plataforma para la creación, edición y compartición de videos cortos. Nuestros servicios están sujetos a cambios y actualizaciones sin previo aviso."
	},
	userObligations: {
		title: "Obligaciones del Usuario",
		p1: "Los usuarios se comprometen a utilizar nuestros servicios de manera responsable y legal. Está prohibido subir contenido que infrinja derechos de autor, sea difamatorio, obsceno o viole la privacidad de terceros."
	},
	intellectualProperty: {
		title: "Propiedad Intelectual",
		p1: "Todo el contenido generado por Yekar, incluyendo pero no limitado a logotipos, diseños y software, es propiedad exclusiva de Yekar. Los usuarios mantienen la propiedad de su contenido, pero otorgan a Yekar una licencia para usar, modificar y distribuir dicho contenido en relación con nuestros servicios."
	},
	limitation: {
		title: "Limitación de Responsabilidad",
		p1: "Yekar no se hace responsable de ningún daño directo, indirecto, incidental o consecuente que resulte del uso o la imposibilidad de usar nuestros servicios."
	},
	termination: {
		title: "Terminación del Servicio",
		p1: "Yekar se reserva el derecho de terminar o suspender su cuenta y acceso a los servicios en cualquier momento, por cualquier motivo, sin previo aviso."
	},
	changes: {
		title: "Cambios en los Términos",
		p1: "Nos reservamos el derecho de modificar estos Términos de Servicio en cualquier momento. Los cambios entrarán en vigor inmediatamente después de su publicación en nuestro sitio web."
	},
	governing: {
		title: "Ley Aplicable",
		p1: "Estos Términos de Servicio se regirán e interpretarán de acuerdo con las leyes de España, sin tener en cuenta sus disposiciones sobre conflictos de leyes."
	},
	contact: {
		title: "Contacto",
		p1: "Si tiene alguna pregunta sobre estos Términos de Servicio, por favor contáctenos en support@yekar.es."
	}
};
var cookiePolicy = {
	title: "Política de Cookies",
	info: {
		title: "Información sobre Cookies",
		p1: "El dominio https://yekar.es (en adelante YEKAR.ES) utiliza procedimientos automáticos de recogida de Cookies para reunir información personal como tipo de navegador o sistema operativo, página de referencia, ruta, dominio ISP, etc. Todo esto con el fin de mejorar los servicios prestados y adaptar este sitio web a sus necesidades personales, ofreciéndole una mejor experiencia de usuario."
	},
	what: {
		title: "¿Qué son las cookies?",
		p1: "Una cookie es un fichero inofensivo de texto que se almacena en su navegador (Chrome, Firefox, etc.) cuando visita casi cualquier página web.",
		p2: "La finalidad de la cookie es que el sitio web que visita recuerde su visita cuando vuelva a navegar por esa página, facilitando la navegación y haciéndola más útil. Como sitio web, nos ayuda a mejorar la calidad permitiéndonos personalizar en cierta medida la navegación de cada usuario.",
		p3: "Aunque mucha gente no lo sabe, las cookies se llevan utilizando desde hace décadas. En la actualidad, son fundamentales para el funcionamiento de Internet, aportando innumerables ventajas en la prestación de servicios interactivos y facilitando la navegación.",
		p4: "Recuerde que las cookies no pueden dañar su ordenador y que, a cambio, el que estén activadas nos ayuda a identificar y resolver los errores, mejorando la navegabilidad del sitio y proporcionando una mejor experiencia a los usuarios."
	},
	notCookie: {
		title: "¿Qué NO es una cookie?",
		p1: "Una Cookie no es un virus, ni un troyano, ni un gusano, ni spam, ni spyware, ni una ventana emergente."
	},
	storedInfo: {
		title: "¿Qué información almacena una Cookie?",
		p1: "Las cookies no suelen almacenar información sensible sobre usted, como tarjetas de crédito o datos bancarios, fotografías, su DNI o información personal, etc.",
		p2: "Los datos que guardan son de carácter técnico, preferencias personales, personalización de contenidos, etc. Por ejemplo, el idioma que utiliza para navegar o el tamaño de letra.",
		p3: "El servidor web no le asocia a usted como persona sino a su navegador web. De hecho, si usted navega habitualmente con Firefox y prueba a navegar por la misma web con otro navegador, como Microsoft Edge o Chrome, verá que la web no se da cuenta de que es usted la misma persona porque en realidad está asociando al navegador, no a la persona."
	},
	types: {
		title: "¿Qué tipos de cookies existen?",
		p1: "Las cookies se pueden dividir en cookies de sesión o cookies permanentes, dependiendo de cuánto tiempo permanezcan instaladas. Las cookies de sesión expiran cuando el usuario cierra el navegador, mientras que las cookies permanentes expiran cuando han cumplido su propósito o se eliminan manualmente.",
		necessary: {
			title: "1) Cookies necesarias o técnicas:",
			p1: "Son estrictamente necesarias para el correcto funcionamiento de la página web. Suelen generarse cuando el usuario accede al sitio web o inicia sesión en el mismo.",
			p2: "Permiten, entre otras cosas, determinar si es un humano o una aplicación automatizada la que navega, si es un usuario anónimo o registrado, tareas básicas para el funcionamiento de cualquier web dinámica.",
			p3: "También mantienen al usuario identificado, de modo que, si abandona la página web y vuelve más tarde, el navegador o dispositivo seguirá reconociéndolo, facilitando así su navegación sin tener que volver a identificarse."
		},
		preferences: {
			title: "2) Cookies de preferencias:",
			p1: "Registran información relacionada con el comportamiento o apariencia del sitio web, como el idioma utilizado o la región desde la que se accede."
		},
		analytics: {
			title: "3) Cookies estadísticas/analíticas:",
			p1: "Se utilizan para analizar y mejorar la experiencia de navegación, optimizar el funcionamiento del sitio web y ver cómo interactúan los visitantes. Recopilan información sobre el tipo de navegación que realiza, las secciones que más utiliza, productos consultados, franja horaria de uso, idioma, etc."
		},
		marketing: {
			title: "4) Cookies de marketing:",
			p1: "Estas cookies se utilizan para mostrar anuncios en el sitio web, vídeos o redes sociales que puedan ser de su interés, en lugar de anuncios aleatorios. El interés potencial se infiere en base a sus preferencias de navegación, país de origen o idioma. También son cookies que recogen información sobre los anuncios mostrados a los usuarios del sitio web."
		},
		geolocation: {
			title: "5) Cookies de geolocalización:",
			p1: "Estas cookies se utilizan para determinar el país o la región donde se encuentra el usuario que accede a un servicio del sitio web, con el fin de ofrecer contenidos o servicios adecuados a su ubicación."
		}
	},
	firstThirdParty: {
		title: "¿Qué son las cookies propias y las de terceros?",
		p1: "Las cookies propias son las generadas por la página web que está visitando, mientras que las de terceros son las generadas por servicios o proveedores externos como Facebook, Twitter o Google."
	},
	disabling: {
		title: "¿Qué ocurre si desactivo las Cookies?",
		p1: "Para entender el alcance que puede tener desactivar las cookies, aquí tiene unos ejemplos:",
		examples: [
			"No podrá compartir contenidos de esa web en Facebook, Twitter o cualquier otra red social.",
			"El sitio web no podrá adaptar los contenidos a sus preferencias personales, como suele ocurrir en las tiendas online.",
			"No podrá acceder al área personal de esa web, como por ejemplo Mi cuenta, o Mi perfil o Mis pedidos.",
			"Tiendas online: Le será imposible realizar compras online, tendrán que ser telefónicas o visitando la tienda física si es que dispone de ella.",
			"No será posible personalizar sus preferencias geográficas como franja horaria, divisa o idioma.",
			"El sitio web no podrá realizar analíticas web sobre visitantes y tráfico en la web, lo que dificultará que la web sea competitiva.",
			"No podrá escribir en el blog, no podrá subir fotos, publicar comentarios, valorar o puntuar contenidos. La web tampoco podrá saber si usted es un humano o una aplicación automatizada que publica spam.",
			"No se podrá mostrar publicidad sectorizada, lo que reducirá los ingresos publicitarios de la web.",
			"Todas las redes sociales usan cookies, si las desactiva no podrá utilizar ninguna red social."
		]
	},
	deletion: {
		title: "¿Se pueden eliminar las cookies?",
		p1: "La respuesta es sí. No sólo se pueden eliminar, sino que es recomendable hacerlo con frecuencia. Las cookies pueden eliminarse o bloquearse, ya sea de forma general o específica para un dominio determinado.",
		p2: "Para eliminar las cookies de un sitio web debe ir a la configuración de su navegador y buscar las asociadas al dominio en cuestión y proceder a su eliminación."
	},
	management: {
		title: "Configuración y gestión de cookies",
		p1: "Para más información sobre cómo personalizar la configuración de las cookies o acceder a las opciones de activación, restricción y/o desactivación, puede consultar la sección de ayuda de su navegador:",
		browsers: [
			{
				name: "Chrome",
				link: "https://support.google.com/chrome/answer/95647?hl=es"
			},
			{
				name: "Firefox",
				link: "https://support.mozilla.org/es/kb/proteccion-antirrastreo-mejorada-en-firefox-para-e"
			},
			{
				name: "Internet Explorer",
				link: "https://support.microsoft.com/es-es/help/17442/windows-internet-explorer-delete-manage-cookies"
			},
			{
				name: "Safari",
				link: "https://support.apple.com/es-es/guide/safari/sfri11471/mac"
			},
			{
				name: "Opera",
				link: "https://help.opera.com/en/latest/web-preferences/#cookies"
			}
		]
	},
	update: {
		title: "Actualización de la política e información sobre cookies",
		p1: "El titular de este sitio web se reserva el derecho de modificar esta política para adaptarla a novedades legislativas o jurisprudenciales, así como a prácticas de la industria."
	}
};
var register = {
	title: "¡Únete!",
	alreadyHaveAccount: "¿Ya tienes una cuenta? <a href=\"/api/login\">Haz clic aquí para iniciar sesión</a>.",
	firstName: "Nombre",
	lastName: "Apellido",
	email: "Correo electrónico",
	password: "Contraseña",
	repeatPassword: "Repetir contraseña",
	combinedConsentLabel: "*Acepto la <a href='/privacy-policy' target='_blank'>Política de Privacidad</a>, los <a href='/terms-of-service' target='_blank'>Términos de Servicio</a>, al aceptarlo, doy mi consentimiento para el almacenamiento temporal de videos como se describe (necesario para el servicio) en la <a href='/privacy-policy#video-storage' target='_blank'>Política de Almacenamiento de Videos</a>.",
	consentError: "Debes aceptar nuestras políticas para registrarte.",
	submitButton: "Registrarse con correo electrónico →",
	optionalFieldsDescription: "Añade tu número de teléfono o tu nombre de usuario de Instagram para poder ayudarte de forma personal.",
	phoneNumber: "Número de teléfono (opcional)",
	instagramHandle: "Usuario de Instagram (opcional)",
	alreadyRegistered: "Ya estás registrado",
	loggedInAs: "Has iniciado sesión como",
	continueButton: "Continuar al Panel →",
	logoutButton: "Cerrar sesión",
	errors: {
		passwordsDoNotMatch: "Las contraseñas no coinciden.",
		selectSubscription: "Por favor selecciona un tipo de suscripción.",
		registrationFailed: "El registro falló",
		unknownError: "Ocurrió un error desconocido"
	}
};
var login = {
	title: "¡Hola!",
	noAccount: "¿No tienes una cuenta? <a href='/api/register'>Haz clic aquí para registrarte</a>.",
	email: "Correo electrónico",
	password: "Contraseña",
	submitButton: "Iniciar sesión →",
	emptyFieldsError: "El correo electrónico y la contraseña no deben estar vacíos",
	genericError: "Ha ocurrido un error",
	alreadyLoggedIn: "Ya has iniciado sesión",
	loggedInAs: "Has iniciado sesión como",
	continueButton: "Continuar →",
	logoutButton: "Cerrar sesión"
};
var cancel = {
	title: "Pago Cancelado",
	message: "El pago no ha funcionado.\nPor favor, contacta con nosotros por email (jon@yekar.es) o por WhatsApp (botón de abajo).",
	homeButton: "Volver al Inicio"
};
var success = {
	title: "¡Bienvenido!",
	message: "Gracias por usar Yekar.<br>Ahora puedes iniciar sesión en tu cuenta.",
	loginButton: "Iniciar Sesión"
};
var common = {
	loading: "Cargando...",
	signUpEmail: "Registrarse con email",
	language: "es",
	languagePreference: {
		label: "¿En qué idioma te sientes más cómodo?",
		options: {
			english: "Inglés",
			spanish: "Español"
		}
	}
};
var payment = {
	processing: {
		title: "Procesando tu pago...",
		message: "Por favor espera mientras confirmamos tu suscripción."
	},
	errors: {
		title: "Ha ocurrido un error",
		noSessionId: "No se proporcionó ID de sesión.",
		noSessionAvailable: "ID de sesión no disponible.",
		timeout: "El procesamiento del pago está tardando más de lo esperado. Por favor, verifica tu método de pago o contacta con soporte.",
		processingFailed: "No se pudo procesar tu pago. Por favor, inténtalo de nuevo o contacta con soporte.",
		statusCheckFailed: "Ocurrió un error al verificar el estado del pago. Por favor, contacta con soporte.",
		contactSupport: "Por favor, contacta con soporte para obtener ayuda."
	}
};
var es = {
	accountSettings: accountSettings,
	nav: nav,
	footer: footer,
	privacyPolicy: privacyPolicy,
	termsOfService: termsOfService,
	cookiePolicy: cookiePolicy,
	register: register,
	login: login,
	cancel: cancel,
	success: success,
	common: common,
	payment: payment
};

export { accountSettings, cancel, common, cookiePolicy, es as default, footer, login, nav, payment, privacyPolicy, register, success, termsOfService };
//# sourceMappingURL=es-d8e1eb69.js.map
